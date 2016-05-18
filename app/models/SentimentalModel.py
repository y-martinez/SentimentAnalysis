from app import app

import pandas as pd
import numpy as np
import re,string,json

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

class SentimentalModel:

	class __SentimentalModel:
		test_file = None
		def __init__(self):

			self.train_file = app.config['DATA_FOLDER'] + '/labeledTrainData.tsv'
			self.train = pd.read_csv(self.train_file, header=0, delimiter="\t", quoting=3)

			print "Preprocessing...\n"
			self.train["tokens"] = self.train["review"].apply(preprocessing)

			print "Creating bag of words...\n"
			self.bag_of_words = []
			self.words = []
			for i in range(len(self.train["tokens"])):
				self.bag_of_words.append(" ".join(self.train["tokens"][i]))
				self.words.extend(self.train["tokens"][i])

			self.reviews_good = pd.DataFrame()
			self.reviews_bad = pd.DataFrame()

			self.reviews_good = self.reviews_good.append(self.train[self.train["sentiment"] == 1],
				ignore_index=True)

			self.reviews_bad = self.reviews_bad.append(self.train[self.train["sentiment"] == 0],
				ignore_index=True)

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

		def predictDataset(self):

			self.test = pd.read_csv(self.test_file, header=0, delimiter="\t", quoting=3)

			print "Preprocessing and creating bag of words test...\n"

			self.words_test = self.test["review"].apply(preprocessing)

			self.bag_of_words_test = []
			for i in range(len(self.words_test)):
				self.bag_of_words_test.append(" ".join(self.words_test[i]))
				
			#Test the model
			self.count_test_features = self.countVector.transform(self.bag_of_words_test)
			self.count_test_features = self.count_test_features.toarray()

			self.tfidf_test_features = self.tfidfVector.transform(self.bag_of_words_test)
			self.tfidf_test_features = self.tfidf_test_features.toarray()

			print "Predicting...\n"
			self.result1 = self.forest1.predict(self.count_test_features)

			self.result2 = self.forest2.predict(self.tfidf_test_features)

			print "Saving...\n"
			self.output1 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result1} )
			self.output2 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result2} )

			return True


		def predictReview(self,text):

			self.bag_of_words_test = preprocessing(text)

			#Test the model
			self.count_test_features = self.countVector.transform(self.bag_of_words_test)
			self.count_test_features = self.count_test_features.toarray()

			self.tfidf_test_features = self.tfidfVector.transform(self.bag_of_words_test)
			self.tfidf_test_features = self.tfidf_test_features.toarray()

			self.result1 = self.forest1.predict(self.count_test_features)

			self.result2 = self.forest2.predict(self.tfidf_test_features)

			self.output1 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result1} )
			self.output2 = pd.DataFrame( data={"id":self.test["id"], "sentiment":self.result2} )

			return True

		def frequencies(self):
			self.words_good = []
			self.words_bad = []
			for i in range(12500):
				self.words_good.extend(self.reviews_good["tokens"][i])
				self.words_bad.extend(self.reviews_bad["tokens"][i])

			self.fdistgood = FreqDist(self.words_good)
			self.fdistbad = FreqDist(self.words_bad)
			self.fdist = FreqDist(self.words)

	instance = None

	def __init__(self):
		if SentimentalModel.instance is None:
			SentimentalModel.instance = SentimentalModel.__SentimentalModel()

	def __getattr__(self):
		return getattr(self.instance)

	def testFileData(self):
		return self.instance.predictDataset()

	def testReview(self,text):
		return self.instance.predictReview(text)

	def getExploratory(self):
		good = self.instance.train['sentiment'].value_counts().get(1)
		bad = self.instance.train['sentiment'].value_counts().get(0)

		#Reviews de ejemplo, agarramos los primeros que vimos que fueran cortos
		text_good = self.instance.train['review'][1]
		text_bad = self.instance.train['review'][7]
		res = { 'pie' : [{'labels': ['Buenos','Malos'] , 'values' : [good,bad] , 'type' : 'pie'}] , 'texts' : [text_good,text_bad] }

		return self.toJson(res)

	def getPreprocessing(self):
		self.instance.frequencies()

		self.good = self.instance.fdistgood.most_common(50)
		self.bad = self.instance.fdistbad.most_common(50)
		self.whole = self.instance.fdist.most_common(50)

		self.good = dict(self.good)
		self.bad = dict(self.bad)
		self.whole = dict(self.whole)

		res = { 'whole': [{'x': self.whole.keys(),'y':self.whole.values(),'type':'bar'}],
		'good': [{'x': self.good.keys(),'y':self.good.values(),'type':'bar'}],
		'bad': [{'x': self.bad.keys(),'y':self.bad.values(),'type':'bar'}] }

		return self.toJson(res)

	def getResults(self):
		good_out1 = self.instance.output1['sentiment'].value_counts().get(1)
		bad_bad1 = self.instance.output1['sentiment'].value_counts().get(0)

		good_out2 = self.instance.output2['sentiment'].value_counts().get(1)
		bad_bad2 = self.instance.output2['sentiment'].value_counts().get(0)

		res = { 'out1' : [{'labels': ['Buenos','Malos'] , 'values' : [good_out1,bad_bad1] , 'type' : 'pie'}],
		'out2' : [{'labels': ['Buenos','Malos'] , 'values' : [good_out2,bad_bad2] , 'type' : 'pie'}] }

		return self.toJson(res)

	def toJson(self,data):
		return json.dumps(data)

	def setFileData(self,filename):
		self.instance.test_file = app.config['DATA_FOLDER'] + "/" + filename

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

	return ( words )