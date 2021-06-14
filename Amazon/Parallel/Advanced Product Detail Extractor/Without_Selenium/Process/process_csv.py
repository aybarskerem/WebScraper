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

  if rank>=3:
    return
  else:
    file=files_ro_read[rank]
    myDict[file]={}
    df=pd.read_csv(file+".csv",  quotechar='"')
    merged_df=df.groupby('Product Ratings')['User Reviews'].apply(' '.join).reset_index()
    # for rating in range(1,6):
    #   if rating==5:
    #     myDict[file][rating]=df[df['Product Ratings']==rating]['User Reviews']   

    category_wise_user_reviews=""
    for _, row in merged_df.iterrows():
      #print(row['Product Ratings'])
      #print(row['User Reviews'])
      rating              = row['Product Ratings']
      user_reviews_merged = row['User Reviews']
      category_wise_user_reviews+=user_reviews_merged
      myDict[file][rating]=list(bag_of_words(user_reviews_merged, sortTheOutput=True).items())[:15]
      cloud(user_reviews_merged, category=file, rating=rating)     
    cloud(category_wise_user_reviews, category=file, rating=None)

    #print(myDict)
    with open(file+"_bag_of_words.txt", 'a') as outputFile:
      outputFile.write(json.dumps(myDict,indent=2))
   

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

def bag_of_words(dataframe, sortTheOutput=False):
  counts = dict()
  bag = []

  bag.extend([
    lemmatize_word(word).upper().translate(str.maketrans('','',string.punctuation)) 
    for word in ( nltk.word_tokenize(dataframe) ) 
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
def cloud(dataframe, category, rating):
  bag=[]

  bag.extend([
    lemmatize_word(word).upper().translate(str.maketrans('','',string.punctuation)) 
    for word in ( nltk.word_tokenize(dataframe) ) 
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