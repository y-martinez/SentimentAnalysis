from app import app

import pandas as pd
import numpy as np
import re,string

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

class SentimentalModel:

	class __SentimentalModel:

		def __init__(self):

			self.train_file = app.config['DATA_FOLDER'] + '/labeledTrainData.tsv'
			self.train = pd.read_csv(self.train_file, header=0, delimiter="\t", quoting=3)

			print "Preprocessing...\n"
			self.train["tokens"] = self.train["review"].apply(preprocessing)

			print "Creating bag of words...\n"
			self.bag_of_words = []
			for i in range(len(self.train["tokens"])):
				self.bag_of_words.append(self.train["tokens"][i])

			self.countVector = CountVectorizer(analyzer = "word",
				tokenizer = None,
				preprocessor = None,
				stop_words = None,
				max_features = 5000)

			self.tfidfVector = TfidfVectorizer(analyzer = "word",
				tokenizer = None,
				min_df = 2,
				max_df = 0.95,
				max_features = 5000,
				sublinear_tf = True)

			self.count_train_features = self.countVector.fit_transform(self.bag_of_words)
			self.count_train_features = self.count_train_features.toarray()

			self.tfidf_train_features = self.tfidfVector.fit_transform(self.bag_of_words)
			self.tfidf_train_features = self.tfidf_train_features.toarray()

			print "Creating model of random forest...\n"
			self.forest1 = RandomForestClassifier(n_estimators = 100)
			self.forest1 = self.forest1.fit( self.count_train_features, self.train["sentiment"] )

			self.forest2 = RandomForestClassifier(n_estimators = 100)
			self.forest2 = self.forest2.fit( self.tfidf_train_features, self.train["sentiment"] )

		def __predictDataset(self,filename):

			self.test_file = app.config['DATA_FOLDER'] + "/" + filename
			self.test = pd.read_csv(self.test_file, header=0, delimiter="\t", quoting=3)

			self.bag_of_words_test = test["review"].apply(preprocessing)

			#Test the model
			self.count_test_features = self.countVector.transform(bag_of_words_test)
			self.count_test_features = self.count_test_features.toarray()

			self.tfidf_test_features = self.tfidfVector.transform(bag_of_words_test)
			self.tfidf_test_features = self.tfidf_test_features.toarray()

			self.result1 = self.forest1.predict(count_test_features)

			self.result2 = self.forest2.predict(tfidf_test_features)

			self.output1 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result1} )
			self.output2 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result2} )


		def __predictReview(self,text):
			self.bag_of_words_test = preprocessing(text)

			#Test the model
			self.count_test_features = self.countVector.transform(bag_of_words_test)
			self.count_test_features = self.count_test_features.toarray()

			self.tfidf_test_features = self.tfidfVector.transform(bag_of_words_test)
			self.tfidf_test_features = self.tfidf_test_features.toarray()

			self.result1 = self.forest1.predict(count_test_features)

			self.result2 = self.forest2.predict(tfidf_test_features)

			self.output1 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result1} )
			self.output2 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result2} )


	instance = None

	def __init__(self):
		if SentimentalModel.instance is None:
			SentimentalModel.instance = SentimentalModel.__SentimentalModel()

	def __getattr__(self):
		return getattr(self.instance)

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

	return (" ".join( words ))