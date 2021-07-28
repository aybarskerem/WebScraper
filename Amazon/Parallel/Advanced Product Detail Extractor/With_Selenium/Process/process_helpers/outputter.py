import configs
from . import wordCloud
import json # use json dumps to format dictionaries while printing

def output_timing_results(duration_seconds, numberOfRepeats, startTime, numberOfProcesses=None):
  '''
  Parameters:
    duration_seconds (int):                       The duration of each run of the process function in process_csv.py
    numberOfRepeats  (int):                       The #of times the process function is called for timeit
    startTime        (datetime.datetime object):  The time the process script started
    nprocs           (int):                       #of MPI processes active
 
  Returns:
    Nothing
  '''
  days    = duration_seconds // 86400
  hours   = (duration_seconds % 86400) // 3600
  minutes = ( (duration_seconds % 86400) % 3600 ) // 60
  seconds = ( (duration_seconds % 86400) % 3600 ) % 60

  days, hours, minutes = map(int, [days, hours, minutes])

  with open("ExecutionTimingResults.txt", mode='a') as outputFile:
    outputFile.write("*************\n")

    if configs.IS_MULTIPROCESSED:
      outputFile.write("MULTI-PROCESSED (PARALLEL) EXECUTION\n")
    else:
      outputFile.write("SINGLE-PROCESSED (SERIAL) EXECUTION\n")
    
    if numberOfProcesses:
      outputFile.write("#of processes involved is: {}\n".format(numberOfProcesses))
    else:
      outputFile.write("#of processes involved is: NA\n") 

    outputFile.write("Processed {}% of the file.\n".format(configs.READING_RATIO_FOR_INPUT_CSVs * 100))
    outputFile.write("#of repeats is: {}\n".format(numberOfRepeats))
    outputFile.write("Script execution start date: {0}\n".format(startTime.strftime("%d/%m/%Y, %H:%M:%S")) )
    outputFile.write("Average script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds) )

    print("Average script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds))

def finalize_wordCloud_bagOfWords_sentimentAnalysis_outputs(wordCloudDict, bagOfWords_dict, sentimentAnalysis_dict, df_sentimentAnalysis ):
  # wordCloud
  if wordCloudDict:
    wordCloud.createCloud_from_wordCloudDict(wordCloudDict)
  # bagOfWords
  if bagOfWords_dict:
    with open("BagOfWords_AllCategories.txt", 'w', encoding='utf-8') as outputFile:
      outputFile.write(json.dumps(bagOfWords_dict, indent=2, ensure_ascii=False))
  # sentimentAnalysis
  if sentimentAnalysis_dict: 
    with open("SentimentAnalysis_AllCategories.txt", 'w', encoding='utf-8') as outputFile:
      outputFile.write(json.dumps(sentimentAnalysis_dict, indent=2, ensure_ascii=False))
  if not df_sentimentAnalysis.empty:
    df_sentimentAnalysis.to_csv('AllCategories_Sentiments.csv', index=False, encoding='utf-8', mode='w')