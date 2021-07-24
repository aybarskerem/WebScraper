from unicode_safe_print import unicode_safe_print
from mpi4py import MPI
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string
from collections import OrderedDict
import json # use json dumps to format dictionaries while printing
import re # we can do "import regex" if needed since python re module does not support \K which is a regex resetting the beginning of a match and starts from the current point 
import functools
from datetime import datetime
from aspect_sentiment_analysis   import aspectBased_sentiment_analysis
from polarity_sentiment_analysis import get_overall_sentimentPolarity
import timeit
print = functools.partial(print, flush=True) #flush print functions by default (needed to see outputs of multiple processes in a more correct order)
from configs import *

files_ro_read=['ELECTRONICS (LAPTOPS)', 'SPORTS', 'TOOLS & HOME IMPROVEMENT' ]

startTime = datetime.now()

def main():
  if IS_MULTIPROCESSED:
    print("Parallel execution time")
  else:
    print("Serial Execution time")
  tp = timeit.Timer("process()", "from __main__ import process")
  average_duration_seconds = tp.timeit(number=NUMBER_OR_REPEATS_TIMEIT) / NUMBER_OR_REPEATS_TIMEIT
  output_timing_results(average_duration_seconds, NUMBER_OR_REPEATS_TIMEIT)

def process():
  if IS_MULTIPROCESSED:
    
    # COMM VARIABLES
    global comm, nprocs, rank
    comm = MPI.COMM_WORLD
    nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
    rank = comm.Get_rank()

    if rank < nprocs-1: # if slave
      df_correspondingRows = comm.recv(source=nprocs-1) #process the urls assigned to this slave
      print(df_correspondingRows)
      sentiment_df = handle_wordCloud_bagOfWords_and_getSentimentAnalysisDict(df_correspondingRows)
      comm.send(sentiment_df, dest=0)
    else: # if master     
      all_dfs = None
      category_for_each_row    = []
      subcategory_for_each_row = []
      for file_to_read in files_ro_read:
        curr_df = pd.read_csv(file_to_read+".csv",  quotechar='"', encoding='utf-8')
        category, subcategory = get_category_subcategory(file_to_read)
        category_for_each_row.extend([category]*curr_df.shape[0])
        subcategory_for_each_row.extend([subcategory]*curr_df.shape[0])
        if all_dfs is not None:
          all_dfs = all_dfs.append(curr_df, ignore_index=True)
        else:
          all_dfs = curr_df

      all_dfs['Category']    = category_for_each_row
      all_dfs['Subcategory'] = subcategory_for_each_row
      all_dfs = all_dfs[all_dfs['Product Ratings']!='Product Ratings'] # remove multiple headers (multiple headers can be produced if we run webscraper multiple times to create the output .csv category) 
      all_dfs['Product Ratings']=pd.to_numeric(all_dfs['Product Ratings'], downcast='integer')

      
      ################## LOAD BALANCE THE DATAFRAME ROWS ACROSS ALL PROCESSES ##################
      number_of_rows_to_process=all_dfs.shape[0]
      # number_of_rows_each_process holds the #of rows distributed to each process (e.g. for a total of 299 rows and 3 slave processes: 100, 100 and 99 rows respectively for process 0, 1 and 2 respectively.)
      least_number_of_rows_for_each_process=number_of_rows_to_process//(nprocs-1)
      number_of_processes_with_one_extra_url=number_of_rows_to_process%(nprocs-1)
      number_of_rows_each_process=[least_number_of_rows_for_each_process+1 if i<number_of_processes_with_one_extra_url
                                  else least_number_of_rows_for_each_process
                                  for i in range(nprocs-1)]

      # send relevant portions of the dataframe to corresponding processes (e.g. for 299 dataframes and 3 slave processes:  0:100, 100:200, 200:299 for process 0, 1 and 2 respectively)
      start=0
      end=0
      for proc_index in range(nprocs-1):
        end=number_of_rows_each_process[proc_index]+end
        print("Proccess " + str(proc_index) + " is responsible for the rows between " + str(start) + " and " + str(end))
        comm.send( (all_dfs[start:end]), dest=proc_index)
        start=end

      isFirstTimeOutputting=True
      for proc_index in range(nprocs-1):
        sentiment_df = comm.recv(source=proc_index) 
        insertHeader = False
        mode = 'a'
        if isFirstTimeOutputting:
          isFirstTimeOutputting = False
          insertHeader = True
          mode = 'w'

        sentiment_df.to_csv('AllCategories_Sentiments.csv', index=False, encoding='utf-8', header=insertHeader, mode=mode)
      
      if MINIMAL_SCRIPT_EXECUTION_TIMING_ACTIVE:
        output_timing_results(numberOfReviewProcessed = sentiment_df.shape[0])
    
  else: # IF A SINGLE PROCESS RUNS ONLY
    all_dfs = None
    category_for_each_row    = []
    subcategory_for_each_row = []
    for file_to_read in files_ro_read:
      curr_df = pd.read_csv(file_to_read+".csv",  quotechar='"', encoding='utf-8')
      category, subcategory = get_category_subcategory(file_to_read)
      category_for_each_row.extend([category]*curr_df.shape[0])
      subcategory_for_each_row.extend([subcategory]*curr_df.shape[0])
      if all_dfs is not None:
        all_dfs = all_dfs.append(curr_df, ignore_index=True)
      else:
        all_dfs = curr_df

    all_dfs['Category']    = category_for_each_row
    all_dfs['Subcategory'] = subcategory_for_each_row
    all_dfs = all_dfs[all_dfs['Product Ratings']!='Product Ratings'] # remove multiple headers (multiple headers can be produced if we run webscraper multiple times to create the output .csv category) 
    all_dfs['Product Ratings']=pd.to_numeric(all_dfs['Product Ratings'], downcast='integer')

    sentiment_df = handle_wordCloud_bagOfWords_and_getSentimentAnalysisDict(all_dfs)

    isFirstTimeOutputting=True
    insertHeader = False
    mode = 'a'
    if isFirstTimeOutputting:
      isFirstTimeOutputting = False
      insertHeader = True
      mode = 'w'

    sentiment_df.to_csv('AllCategories_Sentiments.csv', index=False, encoding='utf-8', header=insertHeader, mode=mode)
    

if MINIMAL_SCRIPT_EXECUTION_TIMING_ACTIVE:
  def output_timing_results(duration_seconds, numberOfRepeats):
    days    = duration_seconds // 86400
    hours   = (duration_seconds % 86400) // 3600
    minutes = ( (duration_seconds % 86400) % 3600 ) // 60
    seconds = ( (duration_seconds % 86400) % 3600 ) % 60

    days, hours, minutes = map(int, [days, hours, minutes])

    with open("ExecutionTimingResults.txt", mode='a') as outputFile:
      outputFile.write("*************\n")

      if IS_MULTIPROCESSED:
        outputFile.write("MULTI-PROCESSED (PARALLEL) EXECUTION\n")
      else:
        outputFile.write("SINGLE-PROCESSED (SERIAL) EXECUTION\n")

      outputFile.write("#of repeats is: {}\n".format(numberOfRepeats))
      outputFile.write("Script execution start date: {0}\n".format(startTime.strftime("%d/%m/%Y, %H:%M:%S")) )
      outputFile.write("Average script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds) )

      print("Average script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds))


def handle_wordCloud_bagOfWords_and_getSentimentAnalysisDict(df_correspondingRows):
  global lemma, tokenizer
  lemma = nltk.wordnet.WordNetLemmatizer()
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 

  # print("category is: " + category)
  # print("subcategory is: " + subcategory)

  ################# HANDLE WORD CLOUD #################
  # create_wordCloud(df_correspondingRows)

  ################# HANDLE BAG OF WORDS #################
  bagOfWords_dict = get_bagOfWords_dict(df_correspondingRows)
  with open("BagOfWords_AllCategories.txt", 'w', encoding='utf-8') as outputFile:
    outputFile.write(json.dumps(bagOfWords_dict,indent=2, ensure_ascii=False))

  ################# HANDLE SENTIMENT ANALYSIS #################
  sentimentAnalysis_dict = get_sentimentAnalysis_dict( df_correspondingRows)    
  # with open(category+"_sentiment_analysis.txt", 'w', encoding='utf-8') as outputFile:
  #   outputFile.write(json.dumps(sentimentAnalysis_dict, indent=2, ensure_ascii=False))

  ################# CREATE SENTIMENT ANALYSIS DATAFRAME for a CSV OUTPUT FILE #################
  df_csv = create_sentimentAnalysis_dataframe(sentimentAnalysis_dict)
  return df_csv

def get_category_subcategory(file_to_read):
  ''' 
  Returns cached result if file_to_read processed before using a global dict to hold results to improve performance

  NOTE: We get category and subcategory information from the file name assuming the information inside the parantheses is a subcategory and the rest indicates the category name. A simple string find method would suffice; but I wanted to use a regex :) 
  
  1) NOT USED (This part can be skipped, not used in the code)
  Explanation of the regex "(.*(?=\(.*\)))\(.*\)\K.*":
  NOTE: The regex below works in PHP but not in Python; so instead of the method below, I will just use grouping.
  
  .*(?=\(.*\)) matches until seeing the paranthesed clause;
  Then we group it with () since we are going to start another search after the paranthesed clause; 
  but we need discard the paranthesed part which \K helps us to (\K discards everything found up until this part which is not grouped with ();
  In our case it will discard only the paranthesed clause but not the part before the paranthesed clause that we already grouped)
  and then matches the rest with .* 

  category = regex.search(r'(.*(?=\(.*\)))\(.*\)\K.*', category).group() # match anything which is not in parantheses
  example 'ELECTRONICS (LAPTOPS)' or 'ELECTRONICS (LAPTOPS) ITEMS' ELECTRONICS ITEMS is category and LAPTOPS is subcategory

  2) USED
  Explanation of the regex "(.*)\((.*)\)(.*)" (which is what we use):
  This regex provides what we want like this example: 'ELECTRONICS (LAPTOPS) ITEMS' -> group(1): ELECTRONICS (with possibly trailing spaces), group(2): LAPTOPS, group(3): ITEMS (with possibly leading spaces)
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


def create_wordCloud(df_correspondingRows):
   # create the clouds per rating, CURRENTLY IGNORING THE BRAND NAMES
  groupingCols = ['Category', 'Subcategory' ,'Product Ratings', 'Brand Name']
  grouped_df = df_correspondingRows.sort_values(by=groupingCols, ascending=[True, True, False, True]).groupby(groupingCols, sort=False)
  for name, group in grouped_df:
    category, subcategory, rating, brand_name = name
    rating=int(rating) # rating is an int64 object which is not JSON serializable; convert it to python int
    user_reviews_merged = ""
    for _, row in group.iterrows(): 
      user_reviews_merged += row['User Reviews']
      if MINIMAL_SCRIPT_EXECUTION_TIMING_ACTIVE:
        break
    cloud(user_reviews_merged, category=category, subcategory=subcategory, rating=rating, brand_name=brand_name )

def create_sentimentAnalysis_dataframe(sentiment_analysis_dict):
  col_category=[]
  col_subcategory=[]
  col_product_rating=[]
  col_brand_name=[]
  col_review_sentiment=[]
  col_review=[]
  col_numberOf_positive_sentences=[]
  col_numberOf_neutral_sentences=[]
  col_numberOf_negative_sentences=[]
  col_positive_sentences=[]
  col_neutral_sentences=[]
  col_negative_sentences=[]
  col_aspectWords=[]
  col_reviewAspectWords=[]
  for category in sentiment_analysis_dict:
    for subcategory in sentiment_analysis_dict[category]:
      for rating in sentiment_analysis_dict[category][subcategory]:
        for brand_name in sentiment_analysis_dict[category][subcategory][rating]:
          # review_dict has two keys "content": which is the review and "sentences": which is a dictionary holding positive, neutral and negative sentences and overall sentiment information
          for review_dict in sentiment_analysis_dict[category][subcategory][rating][brand_name]['Reviews']: 
            col_category.append(category)
            col_subcategory.append(subcategory)
            col_product_rating.append(rating)
            col_brand_name.append(brand_name)

            col_review_sentiment.append(review_dict['Review polarity-based sentiment'])
            col_review.append(review_dict['Content'])
            ###################################################################
            positive_sentences = '\n'.join(review_dict['Sentences']["Positive sentences"])
            neutral_sentences  = '\n'.join(review_dict['Sentences']["Neutral sentences"])
            negative_sentences = '\n'.join(review_dict['Sentences']["Negative sentences"])

            col_numberOf_positive_sentences.append(len(positive_sentences))
            col_numberOf_neutral_sentences.append(len(neutral_sentences))
            col_numberOf_negative_sentences.append(len(negative_sentences))

            col_positive_sentences.append(positive_sentences)
            col_neutral_sentences.append(neutral_sentences)
            col_negative_sentences.append(negative_sentences)
            ###################################################################

            col_aspectWords.append("Cargo\nOriginalty\nPackaging\nQuality")
            col_reviewAspectWords.append(review_dict['Review aspect-based sentiment'])
  return pd.DataFrame({'Category': col_category, 'Subcategory':col_subcategory, 'Product Ratings': col_product_rating, 'Brand Name': col_brand_name, "Review Sentiment":col_review_sentiment, "Review":col_review, '#of Positive Sentences': col_numberOf_positive_sentences, '#of Neutral Sentences': col_numberOf_neutral_sentences, '#of Negative Sentences': col_numberOf_negative_sentences, 'Positive Sentences':col_positive_sentences , 'Neutral Sentences':col_neutral_sentences, 'Negative Sentences':col_negative_sentences, 'Aspect': col_aspectWords, 'Review Aspect Sentiment': col_reviewAspectWords }) 

  
def get_sentimentAnalysis_dict(df_correspondingRows):
  sentiment_analysis_dict = OrderedDict()

  groupingCols = ['Category', 'Subcategory' ,'Product Ratings', 'Brand Name']
  grouped_df = df_correspondingRows.sort_values(by=groupingCols, ascending=[True, True, False, True]).groupby(groupingCols, sort=False)
  for name, group in grouped_df:
    category, subcategory, rating, brand_name = name 
    rating=int(rating) # rating is an int64 object which is not JSON serializable; convert it to python int
    no_of_positive_reviews = 0
    no_of_neutral_reviews  = 0
    no_of_negative_reviews = 0
    review_analysis=[]
    for _, row in group.iterrows(): 

      review = row['User Reviews']
      review=review.replace("\n","")  
      review=review.replace("’","'") # change ’ apostrophe to normal one just in case

      review_polarity=get_overall_sentimentPolarity(review)
      if review_polarity == 'positive':
        no_of_positive_reviews+=1
      elif review_polarity == 'neutral':
        no_of_neutral_reviews+=1 
      elif review_polarity == 'negative':
        no_of_negative_reviews+=1 
      
      review_analysis.append(fillAndGetReviewInformation(review, review_polarity))
      
      if MINIMAL_SCRIPT_EXECUTION_TIMING_ACTIVE:
        break
  
    sentiment_analysis_dict.setdefault(category, OrderedDict()).setdefault(subcategory, OrderedDict()).setdefault(rating, OrderedDict())[brand_name] = {
      "#of positive reviews":  no_of_positive_reviews,
      "#of neutral reviews":   no_of_neutral_reviews,
      "#of negative reviews":  no_of_negative_reviews,
      "Reviews" :              review_analysis}
      
  return sentiment_analysis_dict

def get_bagOfWords_dict(df_correspondingRows):

  bag_of_words_dict=OrderedDict()

  groupingCols = ['Category', 'Subcategory' ,'Product Ratings', 'Brand Name']
  grouped_df = df_correspondingRows.sort_values(by=groupingCols, ascending=[True, True, False, True]).groupby(groupingCols, sort=False)
  for name, group in grouped_df:
    category, subcategory, rating, brand_name = name # the name elements are the same inside a group (these elements represent the values of the columns which are the same thoroughout a group)
    rating=int(rating) # rating is an int64 object which is not JSON serializable; convert it to python int
    user_reviews_merged = ""
    for _, row in group.iterrows(): # each row in the group has the same grouped by elements (i.e. 'Category', 'Subcategory' ,'Product Ratings', 'Brand Name' are the same for those in this group)
      user_reviews_merged += row['User Reviews']
      if MINIMAL_SCRIPT_EXECUTION_TIMING_ACTIVE: # if we are timing, process only a review for each brand for each rating (if not process all)
        break
  
    bag_of_words_dict.setdefault(category, OrderedDict()).setdefault(subcategory, OrderedDict()).setdefault(rating, OrderedDict())[brand_name] = list(bag_of_words(user_reviews_merged, sortTheOutput=True).items())[:15]

  return bag_of_words_dict

def fillAndGetReviewInformation(review, review_polarity):
  '''
    Gets a review and fills a dictionary to hold the content of the review, an overall review polarity and polarity-based sentiment analysis for the sentences of this review

    Parameters:
      review (str):           A string which contains sentence(s).
      review_polarity (str):  A string which defines the poloarity of the review. It can be 'positive', 'neutral' or 'negative'.

    Returns a dictionary with the keys 'Review polarity-based sentiment', 'Review aspect-based sentiment', 'Content' and 'Sentences'
    
  '''
  review_dict = {}
  review_dict['Review polarity-based sentiment'] = review_polarity
  review_dict['Review aspect-based sentiment']   = aspectBased_sentiment_analysis(review)
  review_dict['Content']                         = review
  review_dict['Sentences']                       = polarityBased_sentiment_analysis(review)
  return review_dict

def polarityBased_sentiment_analysis(review):
  '''
    Returns a dict containing the polarity information of each sentence along with the sentences themselves given the 'review'.

    Parameters:
      review (str): A string which contains sentence(s).

    Returns:
      sentence_wise_sentiment_dict: A dictionary containing polarity statistics (positive, neutral, negative) based on each sentence in the 'review' parameter.
    '''
  no_of_positive_sentences = 0
  no_of_neutral_sentences   = 0
  no_of_negative_sentences = 0
  positive_sentences=[]
  negative_sentences=[]
  neutral_sentences=[]
  sentence_wise_sentiment_dict={}
  sentences=tokenizer.tokenize(review)
  for sentence in sentences:
    sentence_sentiment_value=get_overall_sentimentPolarity(sentence)
    if sentence_sentiment_value == 'positive':
      positive_sentences.append(sentence)
      no_of_positive_sentences+=1
    elif sentence_sentiment_value == 'neutral':
      neutral_sentences.append(sentence)
      no_of_neutral_sentences+=1 
    elif sentence_sentiment_value == 'negative':
      negative_sentences.append(sentence)
      no_of_negative_sentences+=1
    
  overall_sentence_sentiment_counts_string = \
    "#of positive sentences: " + str(no_of_positive_sentences) + " - " + \
    "#of neutral sentences:  " + str(no_of_neutral_sentences)  + " - " + \
    "#of negative sentences: " + str(no_of_negative_sentences)

  sentence_wise_sentiment_dict = {
    "Sentences sentiment statistics": overall_sentence_sentiment_counts_string,
    "Positive sentences": positive_sentences, 
    "Neutral sentences": neutral_sentences, 
    "Negative sentences": negative_sentences}

  return sentence_wise_sentiment_dict
  

def is_noun(tag):
  return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def isWordNoun(param_word):
  for word, tag in nltk.pos_tag(nltk.word_tokenize(param_word)): # there is only one item
    return is_noun(tag)

def lemmatize_word(param_word):
  retVal=""
  for word, tag in nltk.pos_tag(nltk.word_tokenize(param_word) ):
      wntag = tag[0].lower()
      wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
      if wntag is None:
          retVal = word
      else:
          retVal = lemma.lemmatize(word, wntag)            
      return retVal

  
def bag_of_words(sentence, sortTheOutput=False):
  counts = dict()
  bag = []

  bag.extend([
    lemmatize_word(word).upper().translate(str.maketrans('','',string.punctuation)) 
    for word in ( nltk.word_tokenize(sentence) ) 
    if isWordNoun(lemmatize_word(word))])
        
  for word in bag:
    if word != "":
      counts[word] = counts.get(word,0)+1      
    
  # sort by values of the dictionary, in an ascending order.
  # We have to use OrderedDict since a normal dict does not preserve orders (sorted returns a list and we have to convert it to a dictionary while preserving the order)
  if sortTheOutput:
    return OrderedDict(sorted(counts.items(), key=lambda key_value_pair: key_value_pair[1], reverse=True))
  else:
    return counts

# if rating is None, it means all ratings combined.
def cloud(sentence, category=None, subcategory=None, rating=None, brand_name=None):
  bag=[]

  bag.extend([
    lemmatize_word(word).upper().translate(str.maketrans('','',string.punctuation)) 
    for word in ( nltk.word_tokenize(sentence) ) 
    if isWordNoun(lemmatize_word(word))])
  bag_str=" ".join(bag)
  wordcloud = WordCloud(background_color="orange").generate(bag_str)
  
  plt.imshow(wordcloud)      
  plt.axis("off")

  if(category is not None and subcategory is not None and rating is not None and brand_name is not None):
    plt.title   (category + "_" + subcategory + "_" + brand_name + "_with_" + str(rating) + " stars")
    plt.savefig (category + "_" + subcategory + "_" + brand_name + "_with_" + str(rating) + " stars")

if __name__ == "__main__":
  main()