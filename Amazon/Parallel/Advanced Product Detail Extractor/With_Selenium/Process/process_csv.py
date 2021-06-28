from mpi4py import MPI
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from regex.regex import sub
from wordcloud import WordCloud
import string
from collections import OrderedDict
import json # use json dumps to format dictionaries while printing
from nltk.sentiment import SentimentIntensityAnalyzer
import re # we can do "import regex" if needed since python re module does not support \K which is a regex resetting the beginning of a match and starts from the current point 
import functools
print = functools.partial(print, flush=True) #flush print functions by default (needed to see outputs of multiple processes in a more correct order)


files_ro_read=['ELECTRONICS (LAPTOPS)', 'SPORTS', 'TOOLS & HOME IMPROVEMENT' ]
lemma = nltk.wordnet.WordNetLemmatizer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def main():

    # # send relevant portions of the url list to corresponding processes (e.g. for 299 pages and 3 slave processes:  0:100, 100:200, 200:299 
    # df = pd.DataFrame({'Processor ID':proc_index, 'Category':CATEGORY, 'Product Names':data['product_names'],'Product Prices':data['product_prices'],'Product Ratings':data['product_ratings'],'User Reviews':data['user_reviews']}) 
    # df.to_csv('amazon_parallel.csv', index=False, encoding='utf-8', mode='a') # append to category

  #myDict=collections.defaultdict(dict)
  
  # COMM VARIABLES
  comm = MPI.COMM_WORLD
  nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
  rank = comm.Get_rank()

  bag_of_words_dict={} 
  sentiment_analysis_dict={} 

  if rank>3:
    return
  else:
    if rank==0: # downloading only in one process is enough (the master processor)
      # make initializations
      nltk.download('vader_lexicon')
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

        df.to_csv('AllCategories_Sentiments.csv', index=False, encoding='utf-8-sig', header=insertHeader, mode=mode) # append to file
    else:
      comm.recv(source=0) # no need to check return value, we only True to indicate initialization is complete

      file_ro_read = files_ro_read[rank-1]
      ''' 
        NOTE: We get category and subcategory information from the file name assuming the information inside the parantheses is a subcategory and the rest indicates the category name. A simple string find method would suffice; but I wanted to use a regex :) 
        
        1) NOT USED
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
      df=pd.read_csv(file_ro_read+".csv",  quotechar='"')
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
            review_sentiment_value=get_overall_sentiment(review)
            if review_sentiment_value == 'positive':
              no_of_positive_reviews+=1
            elif review_sentiment_value == 'neutral':
              no_of_neutral_reviews+=1 
            elif review_sentiment_value == 'negative':
              no_of_negative_reviews+=1 
            
            review_analysis.append(fillAndGetReviewInformation(review, review_sentiment_value))
          
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
      for category in sentiment_analysis_dict:
        for rating in sentiment_analysis_dict[category]:
          for brand_name in sentiment_analysis_dict[category][rating]:
            # review_dict has two keys "content": which is the review and "sentences": which is a dictionary holding positive, neutral and negative sentences and overall sentiment information
            for review_dict in sentiment_analysis_dict[category][rating][brand_name]['Reviews']: 
      
              col_category.append(category)
              col_subcategory.append(subcategory)
              col_product_rating.append(rating)
              col_brand_name.append(brand_name)

              col_review_sentiment.append(review_dict['Review sentiment'])
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

      df = pd.DataFrame({'Category': col_category, 'Subcategory':col_subcategory, 'Product Ratings': col_product_rating, 'Brand Name': col_brand_name, "Review Sentiment":col_review_sentiment, "Review":col_review, '#of Positive Sentences': col_numberOf_positive_sentences, '#of Neutral Sentences': col_numberOf_neutral_sentences, '#of Negative Sentences': col_numberOf_negative_sentences, 'Positive Sentences':col_positive_sentences , 'Neutral Sentences':col_neutral_sentences, 'Negative Sentences':col_negative_sentences, 'Aspect': col_aspectWords  }) 
      
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


'''
Gets a review and fills a dictionary to hold the content of the review, an overall review sentiment and sentiment analysis for sentences of this review
returns a dictionary with the keys 'Review Sentiment, 'Content' and 'Sentences'
'''
def fillAndGetReviewInformation(review, review_sentiment_value):
  review_dict = {}
  review_dict['Review sentiment'] = review_sentiment_value
  review_dict['Content'] = review
  review_dict['Sentences'] = sentence_analysis(review)
  return review_dict

def sentence_analysis(review):
  no_of_positive_sentences = 0
  no_of_neutral_sentences   = 0
  no_of_negative_sentences = 0
  positive_sentences=[]
  negative_sentences=[]
  neutral_sentences=[]
  sentence_wise_sentiment_dict={}
  sentences=tokenizer.tokenize(review)
  for sentence in sentences:
    sentence_sentiment_value=get_overall_sentiment(sentence)
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
  

# remove \u2019 -> utf-16 ; convert this to utf-8
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

   #remove /n u2019 etc 
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