from nltk.sentiment import SentimentIntensityAnalyzer

def get_overall_sentimentPolarity(text):
  '''
    Returns positive, neutral or negative as string values depending on the overall sentiment polarity of the given text.

    Parameters:
      text (str): A string which can be a review (a group of sentences) or a sentence.
    
    Returns:
      'positive', 'negative' or 'neutral' depending on the given text
  '''

  # SentimentIntensityAnalyzer's polarity_scores function outputs positive, negative, neutral and compound value
  #   We can just look at the compound value to get an overall estimation:
  #     positive: compound score >= 0.05
  #     neutral:  compound score between -0.05 and 0.05
  #     negative: compound score <= -0.05
  overall_sentiment_value = SentimentIntensityAnalyzer().polarity_scores(text)['compound']

  if(overall_sentiment_value>=0.05):
    return 'positive'
  elif(overall_sentiment_value<=-0.05):
    return 'negative'
  else:
    return 'neutral'