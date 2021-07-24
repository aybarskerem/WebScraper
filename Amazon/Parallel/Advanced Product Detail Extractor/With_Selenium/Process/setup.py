import stanza
import nltk

stanza.download('en') # about 412 MB in size. Must be downloaded before using aspectBased_sentiment_analysis funciton
nltk.download('vader_lexicon') 
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
