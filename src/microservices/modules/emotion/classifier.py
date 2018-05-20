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
        'cleaned_emotion_dataset.csv')) as f:
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

emotionArr = {}
emotionArr[0,0,0] = "Boredom"
emotionArr[1,0,0] = "Contempt"
emotionArr[0,1,0] = "Fear"
emotionArr[0,0,1] = "Distress"
emotionArr[1,1,0] = "Joy"
emotionArr[1,0,1] = "Surprise"
emotionArr[0,1,1] = "Anger"
emotionArr[1,1,1] = "Interest"

class EmotionCube:

    def __init__(self):
        self.serotonin = 0
        self.dopamine = 0
        self.noradrenaline = 0
        self.emotionMovement = 0.2

    def classifyFeeling(self):
        return emotionArr[round(self.serotonin), round(self.dopamine), round(self.noradrenaline)]

    def updateFeelings(self, emotion):
        if emotion == "anger": #anger makes fear
            self.serotonin -= self.emotionMovement
            self.dopamine += self.emotionMovement
            self.noradrenaline -= self.emotionMovement
        elif emotion == "boredom": #boredom makes boredom
            self.serotonin -= self.emotionMovement
            self.dopamine -= self.emotionMovement
            self.noradrenaline -= self.emotionMovement
        elif emotion == "empty": #empty makes distress
            self.serotonin -= self.emotionMovement
            self.dopamine -= self.emotionMovement
            self.noradrenaline += self.emotionMovement
        elif emotion == "enthusiasm": #makes happy
            self.serotonin += self.emotionMovement
            self.dopamine += self.emotionMovement
            self.noradrenaline -= self.emotionMovement
        elif emotion == "fear": #makes noradrenalin raise
            self.noradrenaline += self.emotionMovement
        elif emotion == "happiness": #makes joy raise 
            self.serotonin += self.emotionMovement
            self.dopamine += self.emotionMovement
            self.noradrenaline -= self.emotionMovement
        elif emotion == "hate": #makes d lower, n rise
            self.dopamine -= self.emotionMovement
            self.noradrenaline += self.emotionMovement
        elif emotion == "love": #makes seratonin rise
            self.serotonin -= self.emotionMovement
        elif emotion == "neutral": #drops all 
            self.serotonin -= self.emotionMovement
            self.dopamine -= self.emotionMovement
            self.noradrenaline -= self.emotionMovement
        elif emotion == "relief": #makes interest
            self.serotonin += self.emotionMovement
            self.dopamine += self.emotionMovement
            self.noradrenaline += self.emotionMovement
        elif emotion == "sadness": #makes joy (cheer up)
            self.serotonin += self.emotionMovement
            self.dopamine += self.emotionMovement
            self.noradrenaline -= self.emotionMovement
        elif emotion == "worry": #makes distress
            self.serotonin -= self.emotionMovement
            self.dopamine -= self.emotionMovement
            self.noradrenaline += self.emotionMovement
        self.serotonin = max(min(self.serotonin, 1), 0)
        self.dopamine = max(min(self.dopamine, 1), 0)
        self.noradrenaline = max(min(self.noradrenaline, 1), 0)

emotionCube = EmotionCube()
def classify(text):
    if(type(text) == list):
        text = " ".join(text)
    if(type(text) == str and len(text) > 0):
        remotion = clf.predict(count_vect.transform([text]))[0].replace("\n", "")
        emotionCube.updateFeelings(remotion)
        return remotion
    return ""

def mood():
    return emotionCube.classifyFeeling()
