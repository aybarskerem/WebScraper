from mpi4py import MPI
from numpy.lib.type_check import mintypecode
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string
#import collections
from collections import OrderedDict
import json # use json dumps to format dictionaries while printing
from nltk.sentiment import SentimentIntensityAnalyzer
import os

files_ro_read=['electronics', 'sports', 'tools' ]

lemma = nltk.wordnet.WordNetLemmatizer()
def main():

    # # send relevant portions of the url list to corresponding processes (e.g. for 299 pages and 3 slave processes:  0:100, 100:200, 200:299 
    # df = pd.DataFrame({'Processor ID':proc_index, 'Category':CATEGORY, 'Product Names':data['product_names'],'Product Prices':data['product_prices'],'Product Ratings':data['product_ratings'],'User Reviews':data['user_reviews']}) 
    # df.to_csv('amazon_parallel.csv', index=False, encoding='utf-8', mode='a') # append to file

  #myDict=collections.defaultdict(dict)
  
  # COMM VARIABLES
  comm = MPI.COMM_WORLD
  nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
  rank = comm.Get_rank()

  myDict={} 
  sentiment_analysis_dict={} 

  if rank==0: # downloading only in one process is enough
    nltk.download('vader_lexicon')

  if rank>=3:
    return
  else:
    file=files_ro_read[rank]
    myDict[file]=OrderedDict()
    sentiment_analysis_dict[file]=OrderedDict()
    df=pd.read_csv(file+".csv",  quotechar='"')
    rating_sorted_df=df.sort_values('Product Ratings', ascending=False)
    merged_df=df.groupby('Product Ratings')['User Reviews'].apply(' '.join).reset_index()

    
    category_wise_user_reviews=""
    for _, row in merged_df.iterrows():
      rating              = row['Product Ratings']
      user_reviews_merged = row['User Reviews']
      category_wise_user_reviews+=user_reviews_merged
      myDict[file][rating]=list(bag_of_words(user_reviews_merged, sortTheOutput=True).items())[:15]
      cloud(user_reviews_merged, category=file, rating=rating)     
    cloud(category_wise_user_reviews, category=file, rating=None)

    #print(myDict)
    with open(file+"_bag_of_words.txt", 'w') as outputFile:
      outputFile.write(json.dumps(myDict,indent=2))

    
    for _, row in rating_sorted_df.iterrows():
      rating       = row['Product Ratings']
      user_reviews = row['User Reviews']
      sentiment_analysis_dict[file].setdefault(rating,[]).append(get_overall_sentiment(user_reviews))
   
    for rating in sentiment_analysis_dict[file]:
      no_of_positives = 0
      no_of_neutrals  = 0
      no_of_negatives = 0
      for sentiment_value in sentiment_analysis_dict[file][rating]:
        if sentiment_value == 'positive':
          no_of_positives+=1
        elif sentiment_value == 'neutral':
          no_of_neutrals+=1 
        elif sentiment_value == 'negative':
          no_of_negatives+=1
      sentiment_analysis_dict[file][rating][0:0]= [
      "#of positives: " + str(no_of_positives),
      "#of neutrals:  " + str(no_of_neutrals), 
      "#of negatives: " + str(no_of_negatives)]

    with open(file+"_sentiment_analysis.txt", 'w') as outputFile:
      outputFile.write(json.dumps(sentiment_analysis_dict,indent=2))


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


def get_overall_sentiment(sentence):
  '''
    returns positive, neutral or negative as string values depending on the overall sentiment of the sentence
  '''
  overall_sentiment_value = sentiment_analysis(sentence)['compound']
  if(overall_sentiment_value>=0.05):
    return 'positive'
  elif(overall_sentiment_value<=-0.05):
    return 'negative'
  else:
    return 'neutral'
  

def sentiment_analysis(sentence):
  '''
  Output positive, negative, neutral and compound value
  We can just look at the compound value to get an overall estimation:
    positive: compound score >= 0.05
    neutral:  compound score between -0.05 and 0.05
    negative: compound score <= -0.05
  '''
  sia = SentimentIntensityAnalyzer()
  return sia.polarity_scores(sentence)

def tf_idf(dataframe):
  '''
    Our documents for tf-idf are the words in separate rating values inside each catagory
    This function calculates td-idf for each category separately. 
    There are 5 possible ratings; so #of documents are 5
    tf:  #of rating values that our word exists (just look at the top-15 entries in rating for a word existence)
    idf: 5 / #of ratings this word is found 
    tf-idf: tf * idf
  '''
  return None
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
def cloud(sentence, category, rating):
  bag=[]

  bag.extend([
    lemmatize_word(word).upper().translate(str.maketrans('','',string.punctuation)) 
    for word in ( nltk.word_tokenize(sentence) ) 
    if isWordNoun(lemmatize_word(word))])
  bag_str=" ".join(bag)
  wordcloud = WordCloud(background_color="orange").generate(bag_str)
  
  plt.imshow(wordcloud)      
  plt.axis("off")

  if(rating is not None):
    plt.title(category+"_with_"+str(rating)+" stars")
    plt.savefig(category+"_with_"+str(rating)+" stars")
  else:
    plt.title(category+"_all_stars_combined")
    plt.savefig(category+"_all_stars_combined")

if __name__ == "__main__":
  main()