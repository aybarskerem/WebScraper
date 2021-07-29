from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 
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