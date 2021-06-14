------------------------------
# DESCRIPTION:

- This script is used to process the output .csv files produced by ../parallel_advancedProductDetail_Extractor.py script using Natural Language Processing techniques.

- This script processes 3 csv files (electronics.csv, tools.csv and sports.csv) which are extracted from ../amazon_parallel.csv according to their categories and outputs .png files for wordclouds and .txt file for bag of word results.

- For wordcloud, each rating is outputted to a different png whereas for bag of words, each rating info is in the indicated as a separate entry in the json string.

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
```
------------------------------
# HOW TO RUN:
An example call is:  
```
mpiexec -n 4 python process_csv.py
```
# INPUTS and OUTPUTS
  
## 1) INPUTS  
  
 - electronics.csv  
 - sports.csv  
 - tools.csv  
  
## 2) OUTPUTS  
  
 - electronics_all_stars_combined.png  
 - electronics_bag_of_words.txt  
 - electronics_with_1 stars.png  
 - electronics_with_2 stars.png  
 - electronics_with_3 stars.png  
 - electronics_with_4 stars.png  
 - electronics_with_5 stars.png  

 - sports_all_stars_combined.png  
 - sports_bag_of_words.txt  
 - sports_with_1 stars.png  
 - sports_with_2 stars.png  
 - sports_with_3 stars.png  
 - sports_with_4 stars.png  
 - sports_with_5 stars.png  

 - tools_all_stars_combined.png  
 - tools_bag_of_words.txt  
 - tools_with_1 stars.png  
 - tools_with_2 stars.png  
 - tools_with_3 stars.png  
 - tools_with_4 stars.png  
 - tools_with_5 stars.png  