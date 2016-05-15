import pandas as pd
import numpy as np
import nltk
from utilities import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

train_file = '../dat/labeledTrainData.tsv'
unlabeled_train_file = '../dat/unlabeledTrainData.tsv'
test_file = '../dat/testData.tsv'

train_labeled = pd.read_csv(train_file,
                         header=0,
                         delimiter="\t", quoting=3)

train_unlabeled = pd.read_csv(unlabeled_train_file,
                         header=0,
                         delimiter="\t", quoting=3)

test_unlabeled = pd.read_csv(test_file, header=0,
                   delimiter="\t",
                   quoting=3 )

print "Preprocessing...\n"
train_labeled["tokens"] = train_labeled["review"].apply(preprocessing)

print "Creating bag of words...\n"
bag_of_words = []
for i in range(len(train_labeled["tokens"])):
	bag_of_words.append(train_labeled["tokens"][i])

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             max_features = 5000)

vectorizer2 = TfidfVectorizer(analyzer = "word", 
							 tokenizer = None,
							 min_df = 2, 
							 max_df = 0.95,
							 max_features = 5000,
							 sublinear_tf = True)
#Train the model
train_data_features = vectorizer.fit_transform(bag_of_words)
train_data_features = train_data_features.toarray()

train_data_features2 = vectorizer2.fit_transform(bag_of_words)
train_data_features2 = train_data_features2.toarray()

print "Creating model of random forest...\n"
forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit( train_data_features, train_labeled["sentiment"] )

forest2 = RandomForestClassifier(n_estimators = 100)
forest2 = forest.fit( train_data_features2, train_labeled["sentiment"] )

print "Creating bag of words test...\n"
bag_of_words_test = test_unlabeled["review"].apply(preprocessing)

#Test the model
test_data_features = vectorizer.transform(bag_of_words_test)
test_data_features = test_data_features.toarray()

test_data_features2 = vectorizer2.transform(bag_of_words_test)
test_data_features2 = test_data_features2.toarray()

print "Predicting...\n"
# Use the random forest to make sentiment label predictions
result = forest.predict(test_data_features)

result2 = forest2.predict(test_data_features2)

print "Save...\n"
output = pd.DataFrame( data={"id":test_unlabeled["id"], "sentiment":result} )
output2 = pd.DataFrame( data={"id":test_unlabeled["id"], "sentiment":result2} )

# Use pandas to write the comma-separated output file
output.to_csv( "Bag_of_Words_model.csv", index=False, quoting=3 )
output2.to_csv( "Bag_of_Words_model2.csv", index=False, quoting=3 )
