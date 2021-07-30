from mpi4py import MPI
import process_helpers.wordCloud as wordCloud
import process_helpers.bagOfWords as bagOfWords
import process_helpers.sentimentAnalysis as sentimentAnalysis
import process_helpers.outputter as outputter
import configs

import pandas as pd
from collections import OrderedDict
import re # we can do "import regex" if needed since python re module does not support \K which is a regex resetting the beginning of a match and starts from the current point 
from datetime import datetime
import timeit
import functools
print = functools.partial(print, flush=True) #flush print functions by default (needed to see outputs of multiple processes in a more correct order)

FILES_TO_READ            = ['ELECTRONICS (LAPTOPS)', 'SPORTS', 'TOOLS & HOME IMPROVEMENT' ] # csv files
START_TIME               = datetime.now()
NUMBER_OF_ROWS_PROCESSED = 0 # set by the master process in multi-processing or by the only process in single-processing in the process() function

def main():
  # COMM VARIABLES
  global comm, nprocs, rank
  comm   = MPI.COMM_WORLD
  nprocs = comm.Get_size() # for multiprocessing there are nprocs-1 slaves (their ranks are 1, 2, ... nprocs-1)  and 1 master (its rank is 0) whereas for single-processing nprocs is 1 and the process' rank is 0.
  rank   = comm.Get_rank() 

  if nprocs > 1:
    if rank == configs.MASTER_PROCESS_RANK: # print it only once
      print("Parallel execution")  
  else:
    print("Serial Execution")

  tp = timeit.Timer("process()", "from __main__ import process") 
  average_duration_seconds = tp.timeit(number=configs.NUMBER_OF_REPEATS_TIMEIT) / configs.NUMBER_OF_REPEATS_TIMEIT # calls process function (for each process) NUMBER_OF_REPEATS_TIMEIT times.

  if (nprocs > 1 and rank == configs.MASTER_PROCESS_RANK) or (nprocs == 1 and rank == 0): 
    outputter.output_timing_results(average_duration_seconds, START_TIME, nprocs, NUMBER_OF_ROWS_PROCESSED)

def process():
  global NUMBER_OF_ROWS_PROCESSED

  if nprocs > 1:
    if rank != configs.MASTER_PROCESS_RANK: # if slave
      df_correspondingRows = comm.recv(source=configs.MASTER_PROCESS_RANK) # process the urls assigned to this slave
      comm.send(get_wordCloud_bagOfWords_dicts_and_getSentimentAnalysis_df(df_correspondingRows) , dest=configs.MASTER_PROCESS_RANK) # send processed results to master
    else: # if master     
      all_dfs = readAllFiles_and_return_df()  
      NUMBER_OF_ROWS_PROCESSED = all_dfs.shape[0]
      print("Total #of rows processed is: {0} ({1}% of each of the input csv file rows are processed)\n".format(NUMBER_OF_ROWS_PROCESSED, configs.READING_RATIO_FOR_INPUT_CSVs * 100))   
      ################## LOAD BALANCE THE DATAFRAME ROWS ACROSS ALL PROCESSES ##################   
      distributed_dfs_forEachProcess, startAndEnds_for_distributed_dfs_forEachProcess = loadBalance_dataframe_toProcesses(all_dfs, nprocs-1)
      
      distributed_dfs_index = 0
      for proc_index in range(nprocs):
        if proc_index != configs.MASTER_PROCESS_RANK:
          print("Proccess {0} is responsible for the rows between {1} and {2}\n".format(proc_index, *startAndEnds_for_distributed_dfs_forEachProcess[distributed_dfs_index] ) )
          comm.send(distributed_dfs_forEachProcess[distributed_dfs_index], dest=proc_index)
          distributed_dfs_index += 1

      wordCloudDict_merged          = {}
      bagOfWords_dict_merged        = OrderedDict()
      sentimentAnalysis_dict_merged = OrderedDict()
      df_sentimentAnalysis_merged   = pd.DataFrame()

      for proc_index in range(nprocs):
        if proc_index != configs.MASTER_PROCESS_RANK:
          wordCloudDict, bagOfWords_dict, sentimentAnalysis_dict, df_sentimentAnalysis = comm.recv(source=proc_index) 
          wordCloud.append_wordCloudDict(wordCloudDict_merged, wordCloudDict)
          bagOfWords.append_bagOfWords_dict(bagOfWords_dict_merged, bagOfWords_dict)
          sentimentAnalysis.append_sentimentAnalysis_dict(sentimentAnalysis_dict_merged, sentimentAnalysis_dict)
          df_sentimentAnalysis_merged = appendAndReturn_df(df_sentimentAnalysis_merged, df_sentimentAnalysis)

      outputter.finalize_wordCloud_bagOfWords_sentimentAnalysis_outputs(wordCloudDict_merged, bagOfWords_dict_merged, sentimentAnalysis_dict_merged, df_sentimentAnalysis_merged)
    
  else: # IF A SINGLE PROCESS RUNS ONLY  (nprocs == 1, process with rank 0) 
    all_dfs = readAllFiles_and_return_df()
    NUMBER_OF_ROWS_PROCESSED = all_dfs.shape[0]
    print("Total #of rows processed is:       {0} ({1}% of each of the input csv file rows are processed)\n".format(NUMBER_OF_ROWS_PROCESSED, configs.READING_RATIO_FOR_INPUT_CSVs * 100))
    wordCloudDict, bagOfWords_dict, sentimentAnalysis_dict, df_sentimentAnalysis  = get_wordCloud_bagOfWords_dicts_and_getSentimentAnalysis_df(all_dfs)

    outputter.finalize_wordCloud_bagOfWords_sentimentAnalysis_outputs(wordCloudDict, bagOfWords_dict, sentimentAnalysis_dict, df_sentimentAnalysis)

def readAllFiles_and_return_df():
  category_for_each_row    = []
  subcategory_for_each_row = []
  df_list = []
  for file_to_read in FILES_TO_READ:
    curr_df                  = read_csv_custom(file_to_read)
    df_list                  .append(curr_df)
    
    category, subcategory    = get_category_subcategory(file_to_read)
    category_for_each_row    .extend( [category]    * curr_df.shape[0] )
    subcategory_for_each_row .extend( [subcategory] * curr_df.shape[0] )
  
  all_dfs = pd.concat(df_list, ignore_index=True)
  all_dfs['Category']        = category_for_each_row
  all_dfs['Subcategory']     = subcategory_for_each_row
  all_dfs = all_dfs[all_dfs['Product Ratings']!='Product Ratings'] # remove multiple headers (multiple headers can be produced if we run webscraper multiple times to create the output .csv category) 
  all_dfs['Product Ratings'] = pd.to_numeric(all_dfs['Product Ratings'], downcast='integer')

  return all_dfs

def appendAndReturn_df(df_merged, df_to_append):
  '''
  pandas dataframe does not support in-place append; so we return the new dataframe
  Assign the result to "df_merged" in the calling function to see the effect (to update the original df_merged)
  '''
  if not df_to_append.empty:
    return df_merged.append(df_to_append, ignore_index=not df_merged.empty)
  return df_merged

def read_csv_custom(file_to_read):
  '''
  Parameters:
    file_to_read (str): csv file name to read without the extension
 
  Returns:
    pandas dataframe as a result of reading the file while also considering 'READING_RATIO_FOR_INPUT_CSVs' config parameter.
  '''
  df = pd.read_csv(file_to_read+".csv",  quotechar='"', encoding='utf-8')
  numberOfRows_toProcess = int(configs.READING_RATIO_FOR_INPUT_CSVs * df.shape[0])
  return df[0:numberOfRows_toProcess]

def loadBalance_dataframe_toProcesses(df_to_distribute, numberOfSlaveProcesses):
  '''
  Parameters:
    - df_to_distribute (pd.DataFrame object) The whole dataframe to be divided among multiple processes
    - numberOfSlaveProcesses (int):          #of worker processes that the dataframe should be distributed to equally (or almost equally) 
 
  Returns:
    - distributed_dfs_forEachProcess:                  A list of pd.DataFrame objects for each process respectively (the object at index 0, 1, 2 represents the dataframe to process for process 0, 1, 2 ... etc.). At each index, this variable contains a certain portion (some rows) of the 'df_to_distribute' input parameter.
    - startAndEnds_for_distributed_dfs_forEachProcess: A list of (start, end) index pairs to know starting / ending rows for each process to process.

  NOTE: This function is only meaningful when nprocs > 1 is True
  '''
  distributed_dfs_forEachProcess                  = []
  startAndEnds_for_distributed_dfs_forEachProcess = []
  number_of_rows_to_process = df_to_distribute.shape[0]
  # number_of_rows_each_process holds the #of rows distributed to each process (e.g. for a total of 299 rows and 3 slave processes: 100, 100 and 99 rows respectively for process 0, 1 and 2 respectively.)
  least_number_of_rows_for_each_process=number_of_rows_to_process // numberOfSlaveProcesses
  number_of_processes_with_one_extra_row=number_of_rows_to_process % numberOfSlaveProcesses
  number_of_rows_each_process=[least_number_of_rows_for_each_process+1 if i<number_of_processes_with_one_extra_row
                              else least_number_of_rows_for_each_process
                              for i in range(numberOfSlaveProcesses)]

  # send relevant portions of the dataframe to corresponding processes (e.g. for 299 dataframes and 3 slave processes:  0:100, 100:200, 200:299 for process 0, 1 and 2 respectively)
  start = 0
  end   = 0
  for slave_proc_index in range(numberOfSlaveProcesses):
    end   = number_of_rows_each_process[slave_proc_index] + end
    startAndEnds_for_distributed_dfs_forEachProcess.append((start, end))
    distributed_dfs_forEachProcess.append(df_to_distribute[start:end])
    start = end
  
  return distributed_dfs_forEachProcess, startAndEnds_for_distributed_dfs_forEachProcess

def get_wordCloud_bagOfWords_dicts_and_getSentimentAnalysis_df(df_correspondingRows):

  # print("category is: " + category)
  # print("subcategory is: " + subcategory)
  wordCloudDict          = {}
  bagOfWords_dict        = OrderedDict()
  sentimentAnalysis_dict = OrderedDict()
  df_sentimentAnalysis   = pd.DataFrame()

  ################# HANDLE WORD CLOUD #################
  if configs.CREATE_WORD_CLOUD:
    wordCloudDict   = wordCloud.get_wordCloudDict_forEachRating(df_correspondingRows)
  ################# HANDLE BAG OF WORDS #################
  if configs.CREATE_BAG_OF_WORDS:
    bagOfWords_dict = bagOfWords.get_bagOfWords_dict(df_correspondingRows)
  ################# HANDLE SENTIMENT ANALYSIS #################
  if configs.CREATE_SENTIMENT_ANALYSIS_RESULTS:
    sentimentAnalysis_dict = sentimentAnalysis.get_sentimentAnalysis_dict( df_correspondingRows)   
    df_sentimentAnalysis   = sentimentAnalysis.create_sentimentAnalysis_dataframe(sentimentAnalysis_dict) # create sentiment analysis dataframe to be outputted to a csv file

  return wordCloudDict, bagOfWords_dict, sentimentAnalysis_dict, df_sentimentAnalysis 

def get_category_subcategory(file_to_read):
  ''' 
  Returns cached result if file_to_read processed before using a global dict to hold results to improve performance

  NOTE: We get category and subcategory information from the file name assuming the information inside the parantheses is a subcategory and the rest indicates the category name. A simple string find method would suffice; but I wanted to use a regex :) 
  
  1) USED (TL;DR)
  Explanation of the regex "(.*)\((.*)\)(.*)" (which is what we use):
  This regex provides what we want like this example: 'ELECTRONICS (LAPTOPS) ITEMS' -> group(1): ELECTRONICS (with possibly trailing spaces), group(2): LAPTOPS, group(3): ITEMS (with possibly leading spaces)

  2) NOT USED (This part can be skipped, not used in the code)
  Explanation of the regex "(.*(?=\(.*\)))\(.*\)\K.*":
  NOTE: The regex below works in PHP but not in Python; so instead of the method below, I will just use grouping.
  
  .*(?=\(.*\)) matches until seeing the paranthesed clause;
  Then we group it with () since we are going to start another search after the paranthesed clause; 
  but we need discard the paranthesed part which \K helps us to (\K discards everything found up until this part which is not grouped with ();
  In our case it will discard only the paranthesed clause but not the part before the paranthesed clause that we already grouped)
  and then matches the rest with .* 

  category = regex.search(r'(.*(?=\(.*\)))\(.*\)\K.*', category).group() # match anything which is not in parantheses
  example 'ELECTRONICS (LAPTOPS)' or 'ELECTRONICS (LAPTOPS) ITEMS' ELECTRONICS ITEMS is category and LAPTOPS is subcategory

  
  '''
  if not hasattr(get_category_subcategory, "category_dict"): #checking category_dict is enough (no need for subcategory_dict too )
    get_category_subcategory.category_dict    = {}
    get_category_subcategory.subcategory_dict = {}

  if file_to_read in get_category_subcategory.category_dict: # return the cached result if any.
    return get_category_subcategory.category_dict[file_to_read], get_category_subcategory.subcategory_dict[file_to_read]

  category = file_to_read
  category_search = re.search(r'(.*)\((.*)\)(.*)', file_to_read) # use search instead of match method since match expects the match to be starting from the beginning 
  if category_search: # if there is no paranthesis, there will be no match. If match; then a subcategory is indicated (in case there is something in paranteses)
    category    = category_search.group(1).strip() +  (" " + category_search.group(3) if category_search.group(3).strip() else "") # if anything comes after paranthesis add it to category as well; if not do not add anything
    subcategory = category_search.group(2).strip() if category_search.group(2) else "General" # if nothing inside the parantheses, assume it is "General"
  else:
    subcategory = "General" 
  
  get_category_subcategory.category_dict[file_to_read]    = category
  get_category_subcategory.subcategory_dict[file_to_read] = subcategory

  return category, subcategory

if __name__ == "__main__":
  main()