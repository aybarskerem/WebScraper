from .aspect_sentiment_analysis   import aspectBased_sentiment_analysis
from .polarity_sentiment_analysis import get_overall_sentimentPolarity, polarityBased_sentiment_analysis
from collections import OrderedDict
import pandas as pd
from configs import *

def append_sentimentAnalysis_dict(sentimentAnalysis_dict_merged, sentimentAnalysis_dict):
  '''
  Parameters:
    sentimentAnalysis_dict_merged ('4 OrderedDict() and then 1 dict() inside' object ) An object which merges multiple sentimentAnalysis_dict object in a special way explained in the 'Description' section.
    sentimentAnalysis_dict        ('4 OrderedDict() and then 1 dict() inside' object )

  Returns 
    Nothing
  
  Description:
    - Updates sentimentAnalysis_dict_merged dictionary with the contents of sentimentAnalysis_dict.
    - This function is used to append a new sentimentAnalysis_dict object to sentimentAnalysis_dict_merged object without loss of data. 
    - We cannot use normal dict.update() method since update() overwrites the value data when the keys are the same; however our values are either integers like the value for "#of positive reviews" key which should be summed or a list as for the key "Reviews" which can be extended with the new sentimentAnalysis_dict's values.
  '''
  if sentimentAnalysis_dict:
    # merge all sentiment analysis dataframes
    if sentimentAnalysis_dict_merged:
      for category in sentimentAnalysis_dict:
        for subcategory in sentimentAnalysis_dict[category]:
          for rating in sentimentAnalysis_dict[category][subcategory]:
            for brand_name in sentimentAnalysis_dict[category][subcategory][rating]:
              sentimentAnalysis_dict_merged.setdefault(category, OrderedDict()).setdefault(subcategory, OrderedDict()).setdefault(rating, OrderedDict()).setdefault(brand_name, {}) # create all keys if not exists before
              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name].setdefault("#of positive reviews", 0)
              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name]["#of positive reviews"] +=  sentimentAnalysis_dict[category][subcategory][rating][brand_name]["#of positive reviews"]

              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name].setdefault("#of neutral reviews", 0)
              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name]["#of neutral reviews"] +=  sentimentAnalysis_dict[category][subcategory][rating][brand_name]["#of neutral reviews"]

              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name].setdefault("#of negative reviews", 0)
              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name]["#of negative reviews"] +=  sentimentAnalysis_dict[category][subcategory][rating][brand_name]["#of negative reviews"]

              sentimentAnalysis_dict_merged[category][subcategory][rating][brand_name].setdefault("Reviews", []).extend( sentimentAnalysis_dict[category][subcategory][rating][brand_name]["Reviews"])            
    else:
      sentimentAnalysis_dict_merged.update(sentimentAnalysis_dict)  


def create_sentimentAnalysis_dataframe(sentiment_analysis_dict):
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
    for subcategory in sentiment_analysis_dict[category]:
      for rating in sentiment_analysis_dict[category][subcategory]:
        for brand_name in sentiment_analysis_dict[category][subcategory][rating]:
          # review_dict has two keys "content": which is the review and "sentences": which is a dictionary holding positive, neutral and negative sentences and overall sentiment information
          for review_dict in sentiment_analysis_dict[category][subcategory][rating][brand_name]['Reviews']: 
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
  return pd.DataFrame({'Category': col_category, 'Subcategory':col_subcategory, 'Product Ratings': col_product_rating, 'Brand Name': col_brand_name, "Review Sentiment":col_review_sentiment, "Review":col_review, '#of Positive Sentences': col_numberOf_positive_sentences, '#of Neutral Sentences': col_numberOf_neutral_sentences, '#of Negative Sentences': col_numberOf_negative_sentences, 'Positive Sentences':col_positive_sentences , 'Neutral Sentences':col_neutral_sentences, 'Negative Sentences':col_negative_sentences, 'Aspect': col_aspectWords, 'Review Aspect Sentiment': col_reviewAspectWords }) 

  
def get_sentimentAnalysis_dict(df_correspondingRows):
  sentiment_analysis_dict = OrderedDict()

  groupingCols = ['Category', 'Subcategory' ,'Product Ratings', 'Brand Name']
  grouped_df = df_correspondingRows.sort_values(by=groupingCols, ascending=[True, True, False, True]).groupby(groupingCols, sort=False)
  for name, group in grouped_df:
    category, subcategory, rating, brand_name = name 
    rating=int(rating) # rating is an int64 object which is not JSON serializable; convert it to python int
    no_of_positive_reviews = 0
    no_of_neutral_reviews  = 0
    no_of_negative_reviews = 0
    review_analysis=[]
    for _, row in group.iterrows(): 

      review = row['User Reviews']
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

    sentiment_analysis_dict.setdefault(category, OrderedDict()).setdefault(subcategory, OrderedDict()).setdefault(rating, OrderedDict())[brand_name] = {
      "#of positive reviews":  no_of_positive_reviews,
      "#of neutral reviews":   no_of_neutral_reviews,
      "#of negative reviews":  no_of_negative_reviews,
      "Reviews" :              review_analysis}
    
  return sentiment_analysis_dict

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
  review_dict['Review aspect-based sentiment']   = aspectBased_sentiment_analysis(review)
  review_dict['Content']                         = review
  review_dict['Sentences']                       = polarityBased_sentiment_analysis(review)
  return review_dict