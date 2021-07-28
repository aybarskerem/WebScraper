import nltk
# Modules are only evaluated the 1st time that they are imported; so it is okay to initialize here without an initialization function which is called only once

lemma = nltk.wordnet.WordNetLemmatizer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')