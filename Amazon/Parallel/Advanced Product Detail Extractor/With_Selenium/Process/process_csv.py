from mpi4py import MPI
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from regex.regex import sub
from wordcloud import WordCloud
import string
from collections import OrderedDict
import json # use json dumps to format dictionaries while printing

import re # we can do "import regex" if needed since python re module does not support \K which is a regex resetting the beginning of a match and starts from the current point 
import functools
from nltk.corpus import stopwords
import stanza # pip install stanza
from aspect_sentiment_analysis   import aspectBased_sentiment_analysis
from polarity_sentiment_analysis import get_overall_sentimentPolarity
import traceback
from unicode_safe_print import unicode_safe_print 
from enum import Enum

print = functools.partial(print, flush=True) #flush print functions by default (needed to see outputs of multiple processes in a more correct order)

files_ro_read=['ELECTRONICS (LAPTOPS)', 'SPORTS', 'TOOLS & HOME IMPROVEMENT' ]


# COMM VARIABLES
comm = MPI.COMM_WORLD
nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
rank = comm.Get_rank()

def main():


  bag_of_words_dict={} 
  sentiment_analysis_dict={} 

  if rank>3:
    return
  else:
    if rank==0: # downloading only in one process is enough (the master processor)
      # make initializations
      nltk.download('vader_lexicon')
      stanza.download('en')
      nltk.download('stopwords')
      nltk.download('punkt')
      nltk.download('averaged_perceptron_tagger')

      for proc_index in range(1, 4):
        comm.send(True, dest=proc_index)

      isFirstTimeOutputting=True
      for proc_index in range(1, 4):
        df = comm.recv(source=proc_index) 
        insertHeader = False
        mode = 'a'
        if isFirstTimeOutputting:
          isFirstTimeOutputting = False
          insertHeader = True
          mode = 'w'

        df.to_csv('AllCategories_Sentiments.csv', index=False, encoding='utf-8', header=insertHeader, mode=mode) # append to file
    else:
      comm.recv(source=0) # no need to check return value, we only True to indicate initialization is complete
      
      global lemma, tokenizer

      lemma = nltk.wordnet.WordNetLemmatizer()
      tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 

      file_ro_read = files_ro_read[rank-1]
      ''' 
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
        
      category = file_ro_read
      category_search = re.search(r'(.*)\((.*)\)(.*)', file_ro_read) # use search instead of match method since match expects the match to be starting from the beginning 
      if category_search: # if there is no paranthesis, there will be no match. If match; then a subcategory is indicated (in case there is something in paranteses)
        category    = category_search.group(1).strip() +  (" " + category_search.group(3) if category_search.group(3).strip() else "") # if anything comes after paranthesis add it to category as well; if not do not add anything
        subcategory = category_search.group(2).strip() if category_search.group(2) else "General" # if nothing inside the parantheses, assume it is "General"
      else:
        subcategory = "General" 

      print("category is: " + category)
      print("subcategory is: " + subcategory)
      bag_of_words_dict[category]=OrderedDict()
      sentiment_analysis_dict[category]=OrderedDict()
      df=pd.read_csv(file_ro_read+".csv",  quotechar='"', encoding='utf-8')
      # filtering out the rows with `POSITION_T` value in corresponding column
      df = df[df['Product Ratings']!='Product Ratings'] # remove multiple headers (multiple headers can be produced if we run webscraper multiple times to create the output .csv category)

      
      df['Product Ratings']=pd.to_numeric(df['Product Ratings'], downcast='integer')
      for rating in range(5,0,-1):
      
        # iterate thru each brand while all the corresponding user reviews for a particular brand are put into a list
        sentiment_analysis_dict[category][rating]={}
        df_brand_and_corresponding_reviews_list=df[df['Product Ratings']==rating].groupby('Brand Name')['User Reviews'].apply(list).reset_index()
        #print(df_brand_and_corresponding_reviews_list)
        
        for _,row in df_brand_and_corresponding_reviews_list.iterrows():      
          user_reviews_list = row['User Reviews']
          brand_name        = row['Brand Name']

          no_of_positive_reviews = 0
          no_of_neutral_reviews  = 0
          no_of_negative_reviews = 0
          review_analysis=[]
          for review in user_reviews_list:
            #print(review)
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
          
          sentiment_analysis_dict[category][rating][brand_name] = {
            "#of positive reviews":  no_of_positive_reviews,
            "#of neutral reviews":   no_of_neutral_reviews,
            "#of negative reviews":  no_of_negative_reviews,
            "Reviews" :              review_analysis}
        # iterate thru each brand while the reviews are merged for each brand (there is only one entry for each brand name and all the corresponding user reviews for a particular brand are merged into a single string)
      #   bag_of_words_dict[category][rating]={}
      #   df_brand_and_corresponding_reviews_combined=df[df['Product Ratings']==rating].groupby('Brand Name')['User Reviews'].apply(' '.join).reset_index()
      #   for _,row in df_brand_and_corresponding_reviews_combined.iterrows():
      #     user_reviews_merged = row['User Reviews']
      #     brand_name          = row['Brand Name']
      #     bag_of_words_dict[category][rating][brand_name]=list(bag_of_words(user_reviews_merged, sortTheOutput=True).items())[:15]

      # #print(myDict)
      # with open(category+"_bag_of_words.txt", 'w', encoding='utf-8') as outputFile:
      #   outputFile.write(json.dumps(bag_of_words_dict,indent=2, ensure_ascii=False))


      with open(category+"_sentiment_analysis.txt", 'w', encoding='utf-8') as outputFile:
        outputFile.write(json.dumps(sentiment_analysis_dict, indent=2, ensure_ascii=False))

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
        for rating in sentiment_analysis_dict[category]:
          for brand_name in sentiment_analysis_dict[category][rating]:
            # review_dict has two keys "content": which is the review and "sentences": which is a dictionary holding positive, neutral and negative sentences and overall sentiment information
            for review_dict in sentiment_analysis_dict[category][rating][brand_name]['Reviews']: 
      
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
      df = pd.DataFrame({'Category': col_category, 'Subcategory':col_subcategory, 'Product Ratings': col_product_rating, 'Brand Name': col_brand_name, "Review Sentiment":col_review_sentiment, "Review":col_review, '#of Positive Sentences': col_numberOf_positive_sentences, '#of Neutral Sentences': col_numberOf_neutral_sentences, '#of Negative Sentences': col_numberOf_negative_sentences, 'Positive Sentences':col_positive_sentences , 'Neutral Sentences':col_neutral_sentences, 'Negative Sentences':col_negative_sentences, 'Aspect': col_aspectWords, 'Review Aspect Sentiment': col_reviewAspectWords }) 
      
      comm.send(df, dest=0)
    
      # create the clouds per rating, CURRENTLY IGNORING THE BRAND NAMES
      # merged_df=df.groupby('Product Ratings')['User Reviews'].apply(' '.join).reset_index()
      # category_wise_user_reviews=""
      # for _, row in merged_df.iterrows():
      #   user_reviews_merged = row['User Reviews']
      #   rating              = row['Product Ratings']
      #   category_wise_user_reviews+=user_reviews_merged
      #   cloud(user_reviews_merged, category=category, rating=rating)     
      # cloud(category_wise_user_reviews, category=category, rating=None)



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
  review_dict['Review aspect-based sentiment'] = aspectBased_sentiment_analysis(review)
  review_dict['Content'] = review
  review_dict['Sentences'] = polarityBased_sentiment_analysis(review)
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
  # try:  
  #   main()
  # except Exception as ex:
  #   print(ex)
  #   traceback.print_exc()
  #   comm.Abort() # if any of the processes throw an error; exit all