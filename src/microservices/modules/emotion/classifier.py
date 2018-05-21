from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import os
import sys

x = []
y = []
with open(os.path.join(
        os.path.abspath(os.path.dirname("__file__")),
        'cleaned_emotion_dataset.csv')) as f: #FIX
    for line in f:
        x.append(line.split(";")[0])
        y.append(line.split(";")[1])


X_train, X_test, y_train, y_test = train_test_split(
    x, y, random_state=0, test_size=0.3)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)


def classify(text):
    if(type(text) == list):
        text = " ".join(text)
    if(type(text) == str and len(text) > 0):
        return clf.predict(count_vect.transform([text]))[0].replace("\n", "")
    return ""
