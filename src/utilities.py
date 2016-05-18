import pandas as pd
import numpy as np
import re,string

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

def preprocessing(raw_review,lang="english"):

	tknzr = TweetTokenizer(reduce_len=True)

	raw_review = re.sub ("<br\s*\/>", " ", raw_review)
	raw_review = re.sub ("\\\\","",raw_review)
	raw_review = re.sub ("\"","",raw_review)

	if lang == "english":
		raw_review = re.sub("\'","",raw_review)

	words = tknzr.tokenize(raw_review)
	punctuation = list(string.punctuation)

	stops = set(stopwords.words(lang) + punctuation)
	words = [word for word in words if not word.lower() in stops]

	return (" ".join(words))

