------------------------------
# DESCRIPTION:

- This script is used to process the output .csv files produced by ../webscraper.py script using Natural Language Processing techniques.  

- This script processes 3 csv files (ELECTRONICS (LAPTOPS).csv, SPORTS.csv and TOOLS & HOME IMPROVEMENT.csv) according to their categories and then outputs .png files for wordclouds and .txt file for bag of word results.  
    
- For wordcloud, each rating is outputted to a different png. As for bag of words, each rating and brand name info is in the indicated as a separate entry in the json string. The json hierarchy for bag of words is input .csv file name, category, rating and at the inner most part brand name.  
     
- The output files can be found in ./outputs folder.  
  
- Since there are lots of tasks that the process script has to do; a modularized approach is adopted and many of the codes are put into functions and each function is put into their corresponding module according to its purpose. All of these helper modules that the process script uses can be found in ./process_helper folder.
  
- Please set the parameters in config file (./configs.py) according to your own preferences. 
  
- Output file 'ExecutionTimingResults.txt' show information regarding to the timing measurements of the script. One can run the script with different configurations (by setting the parameters in the config file) and check the results in this file to see the effect of each parameter.  
    
------------------------------
# DEPENDENCIES:

1) Python3

2) Library Installations (download pip3 first if not installed already):
```
pip install numpy
pip install pandas
pip install wordcloud
pip install nltk
pip install matplotlib
pip install stanza
```

3) setup.py  
Please execute ```python setup.py``` before running the code to install some dependency packages.
------------------------------
# HOW TO RUN:
An example call for multiprocessed execution is (i.e. IS_MULTIPROCESSED config variable is True):  
```
mpiexec -n 4 python process_csv.py
```
  
The call for a single processed execution is (i.e. IS_MULTIPROCESSED config variable is False):  
```
python process_csv.py
```

# INPUTS and OUTPUTS
  
## 1) INPUTS  
  
 - ELECTRONICS (LAPTOPS).csv  
 - SPORTS.csv  
 - TOOLS & HOME IMPROVEMENT.csv  
  
## 2) OUTPUTS  

Output files below can be found in OUTPUTS folder.  

- 1 stars.png  
- 2 stars.png  
- 3 stars.png  
- 4 stars.png  
- 5 stars.png  
- AllCategories_Sentiments.csv  
- BagOfWords_AllCategories.txt  
- ExecutionTimingResults.txt  
- SentimentAnalysis_AllCategories.txt  

## 3) SCRIPT TERMINAL OUTPUT EXAMPLES
  
1) Single-process execution where CREATE_WORD_CLOUD, CREATE_BAG_OF_WORDS and CREATE_SENTIMENT_ANALYSIS_RESULTS are True:  
  
- Serial Execution  
- Total #of rows processed is: 146 (1.0% of each of the input csv file rows are processed)  
- Average script execution duration: 0 days 0 hours 4 minutes 24.124343699999997 seconds  
  
2) Multi-process (4 processes) execution where CREATE_WORD_CLOUD, CREATE_BAG_OF_WORDS and CREATE_SENTIMENT_ANALYSIS_RESULTS are True:  
  
- Parallel execution  
- Total #of rows to process is: 146 (1.0% of each of the input csv file rows are processed) 
- Proccess 1 is responsible for the rows between 0 and 49  
- Proccess 2 is responsible for the rows between 49 and 98  
- Proccess 3 is responsible for the rows between 98 and 146    
- Average script execution duration: 0 days 0 hours 3 minutes 25.5691377 seconds  
  
3) Multi-process (8 processes) execution where CREATE_WORD_CLOUD, CREATE_BAG_OF_WORDS and CREATE_SENTIMENT_ANALYSIS_RESULTS are True: 

- Parallel execution  
- Total #of rows processed is: 146 (1.0% of each of the input csv file rows are processed)  
- Proccess 1 is responsible for the rows between 0 and 21  
- Proccess 2 is responsible for the rows between 21 and 42  
- Proccess 3 is responsible for the rows between 42 and 63  
- Proccess 4 is responsible for the rows between 63 and 84  
- Proccess 5 is responsible for the rows between 84 and 105  
- Proccess 6 is responsible for the rows between 105 and 126  
- Proccess 7 is responsible for the rows between 126 and 146  
- Average script execution duration: 0 days 0 hours 2 minutes 57.8988914 seconds  