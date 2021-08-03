from . import customGlobals
import nltk
from collections import OrderedDict
from itertools import islice # to be able to slice OrderedDict
from configs import *
import string


def append_bagOfWords_dict(bagOfWords_dict_merged, bagOfWords_dict):
  '''
  Parameters:
    bagOfWords_dict_merged ('4 OrderedDict() and then 1 dict() inside' object ) An object which merges multiple bagOfWords_dict object in a special way explained in the 'Description' section.
    bagOfWords_dict        ('4 OrderedDict() and then 1 dict() inside' object )

  Returns 
    Nothing
  
  Description:
    - Updates bagOfWords_dict_merged dictionary with the contents of bagOfWords_dict.
    - This function is used to append a new bagOfWords_dict object to bagOfWords_dict_merged object without loss of data. 
    - We cannot use normal dict.update() method since update() overwrites the value data when the keys are the same; however our values are integers (word frequencies/counts) which should be summed, not overwritten by the bagOfWords_dict's counts .
  '''
  if bagOfWords_dict:
    # update word frequencies/counts in bagOfWords_dict_merged with bagOfWords_dict
    if bagOfWords_dict_merged:
      for category in bagOfWords_dict:
        for subcategory in bagOfWords_dict[category]:
          for rating in bagOfWords_dict[category][subcategory]:
            for brand_name in bagOfWords_dict[category][subcategory][rating]:
              for word, wordFreq in bagOfWords_dict[category][subcategory][rating][brand_name].items():
                bagOfWords_dict_merged.setdefault(category, OrderedDict()).setdefault(subcategory, OrderedDict()).setdefault(rating, OrderedDict()).setdefault(brand_name, {}).setdefault(word, 0) # create all keys if not exist
                bagOfWords_dict_merged[category][subcategory][rating][brand_name][word] += wordFreq

              bagOfWords_dict_merged[category][subcategory][rating][brand_name] = OrderedDict( sorted(bagOfWords_dict_merged[category][subcategory][rating][brand_name].items(), key=lambda key_value_pair: key_value_pair[1], reverse=True) ) # sort the bag of words dictionary according to the new word counts (from highest occurrent word to lowest occurrent)
    else:
      bagOfWords_dict_merged.update(bagOfWords_dict)
    
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
  
    bag_of_words_dict.setdefault(category, OrderedDict()).setdefault(subcategory, OrderedDict()).setdefault(rating, OrderedDict())[brand_name]  = bag_of_words(user_reviews_merged, sortTheOutput=True, sliceStart=0, sliceEnd=15)

  return bag_of_words_dict

  
def bag_of_words(text, sortTheOutput=False, sliceStart=None, sliceEnd=None ):
  '''
  Parameters:
    text (str):    A string which contains sentence(s).
    sortTheOutput: Whether we should we return OrderedDict where the items sorted from the highest occurrent word to the least or a normal Python dict.
    sliceStart: Slice start index to slice OrderedDict, only applicable if sortTheOutput == True
    sliceEnd    Slice end index to slice OrderedDict, only applicable if sortTheOutput == True

  Returns:
    A dictionary (string, int)  key/value pairs where key is the word and value is the frequency of this word in the  input parameter 'text' 

  NOTE:
  Please refer to https://docs.python.org/3/library/itertools.html#itertools.islice to determine sliceStart and sliceEnd values.  
  '''
  counts = dict()
  bag = getProcessedWordArray(text)
  for word in bag:
    if word != "":
      counts[word] = counts.get(word, 0) + 1      
    
  # sort by values of the dictionary, in an ascending order.
  # We have to use OrderedDict since a normal dict does not preserve orders (sorted returns a list and we have to convert it to a dictionary while preserving the order)
  if sortTheOutput:
    orderedDict = OrderedDict( sorted(counts.items(), key=lambda key_value_pair: key_value_pair[1], reverse=True) )
    return OrderedDict( islice(orderedDict.items(), sliceStart, sliceEnd) ) # itemgetter(1) is the same as key=lambda key_value_pair: key_value_pair[1] or itemgetter(1, 3) as key_value_pair: (key_value_pair[1], key_value_pair[3])
  else:
    return counts

def getProcessedWordArray(text):
  bag = []
  bag.extend([
    lemmatize_word(word).upper().translate(str.maketrans('','',string.punctuation)) 
    for word in ( nltk.word_tokenize(text) ) 
    if isWordNoun(lemmatize_word(word))])
  return bag

def is_noun(tag):
  return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def isWordNoun(param_word):
  for word, tag in nltk.pos_tag(nltk.word_tokenize(param_word)): # there is only one item
    return is_noun(tag)

def lemmatize_word(param_word):

  retVal=""
  for word, tag in nltk.pos_tag( nltk.word_tokenize(param_word) ):
      wntag = tag[0].lower()
      wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
      if wntag is None:
          retVal = word
      else:
          retVal = customGlobals.lemma.lemmatize(word, wntag)            
      return retVal