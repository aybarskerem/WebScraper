from . import bagOfWords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from configs import *

def append_wordCloudDict(wordCloudDict_merged, wordCloudDict):
  '''
  Parameters:
    wordCloudDict_merged ( 'dict( dict() )' ): An object which merges multiple wordCloudDict object in a special way explained in the 'Description' section.
    wordCloudDict        ( 'dict ( dict() )' )

  Returns 
    Nothing
  
  Description:
    - Updates wordCloudDict_merged dictionary with the contents of wordCloudDict.
    - This function is used to append a new wordCloudDict object to wordCloudDict_merged object without loss of data. 
    - We cannot use normal dict.update() method since update() overwrites the value data when the keys are the same; however our values are integers (word frequencies/counts) which should be summed, not overwritten by the wordCloudDict's counts.
  '''
  if wordCloudDict:
    if wordCloudDict_merged:
      for rating in wordCloudDict:
        for word, wordFreq in wordCloudDict[rating].items():
          wordCloudDict_merged.setdefault(rating, {}).setdefault(word, 0) # create all keys if not exist
          wordCloudDict_merged[rating][word] += wordFreq
    else:
      wordCloudDict_merged.update(wordCloudDict)

def get_wordCloudDict_forEachRating(df_correspondingRows):
   # create the clouds per rating, CURRENTLY IGNORING THE BRAND NAMES
  wordCloud_dict = {}
  groupingCols = ['Product Ratings']
  grouped_df = df_correspondingRows.sort_values(by=groupingCols, ascending=[True]).groupby(groupingCols, sort=False)
  for name, group in grouped_df:
    rating = name
    rating=int(rating) # rating is an int64 object which is not JSON serializable; convert it to python int
    user_reviews_merged = ""
    for _, row in group.iterrows(): 
      user_reviews_merged += row['User Reviews']
    wordCloud_dict[rating] = bagOfWords.bag_of_words(user_reviews_merged, sortTheOutput=True)
    
  return wordCloud_dict

def createCloud_from_wordCloudDict(wordCloudDict):
  '''
  wordCloudDict: Dictionary of (rating, text) pairs. Output of get_wordCloudDict_forEachRating() function (multiple get_wordCloudDict_forEachRating dicts can be merged as well) 
  rating: to what rating group (1, 2, 3, 4 or 5) this text belongs to
  '''
  for rating in wordCloudDict:
    wordcloud = WordCloud(background_color="orange").generate_from_frequencies(wordCloudDict[rating])
    plt.imshow(wordcloud)      
    plt.axis("off")
    plt.title   (str(rating) + " stars")
    plt.savefig (str(rating) + " stars")