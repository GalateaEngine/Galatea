from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.classifier import Classifier

import pickle
import ujson as json
import os
# Config

emotionclassifier = Classifier(
    pickle.load(
        open(
            os.path.join( os.path.abspath(os.path.dirname(__file__)), "./dataset.dat"),
            "rb")),
    tokenizer)
def classify(text,full_result=False):
    classification = sorted(emotionclassifier.classify(text), key=lambda x: x[1])
    if (full_result==True):
        return classification
    return  classification[-1][0]