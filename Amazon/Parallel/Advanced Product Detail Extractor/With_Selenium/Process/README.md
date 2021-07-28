------------------------------
# DESCRIPTION:

- This script is used to process the output .csv files produced by ../parallel_advancedProductDetail_Extractor.py script using Natural Language Processing techniques.

- This script processes 3 csv files (ELECTRONICS (LAPTOPS).csv, SPORTS.csv and TOOLS & HOME IMPROVEMENT.csv) according to their categories and then outputs .png files for wordclouds and .txt file for bag of word results.

- For wordcloud, each rating is outputted to a different png. As for bag of words, each rating and brand name info is in the indicated as a separate entry in the json string. The json hierarchy for bag of words is input .csv file name, category, rating and at the inner most part brand name.

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