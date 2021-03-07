import collections
import os
import pickle
import re
import pandas as pd
import numpy as np
import joblib
import shutil
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from nltk.tokenize import word_tokenize
import nltk.data

nltk.data.path.append("nltk_data")


def clean_str(text):
    text = re.sub(r"[^A-Za-z0-9(),!?\'\`\"]", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip().lower()

    return text


def build_dataset(datatype='abs'):
    text_list = []
    class_list = []
    if datatype == 'abs':
        pos = "data/pos_abstract"
        neg = "data/neg_abstract"
    else:
        pos = "data/pos_full"
        neg = "data/neg_full"

    for filename in os.listdir(pos):
        content = open(os.path.join(pos, filename)).read()
        text_list.append(content)
        class_list.append(1)

    for filename in os.listdir(neg):
        content = open(os.path.join(neg, filename)).read()
        text_list.append(content)
        class_list.append(0)

    data = {
        "content": text_list,
        "class": class_list
    }

    df = pd.DataFrame(data)
    df = df.sample(frac=1)
    x = list(map(lambda d: word_tokenize(clean_str(d)), df["content"]))
    x = list(" ".join(i) for i in x)

    y = list(df["class"])

    return x, y


class SVM:
    def __init__(self, datatype="abs"):
        self.train_x, self.train_y = build_dataset(datatype)

    def train(self):
        text_clf = Pipeline([("vect", CountVectorizer()),
                             ("tfidf", TfidfTransformer()),
                             ("clf", SVC(C=1, kernel="poly"))])
        text_clf = text_clf.fit(self.train_x, self.train_y)
        print("train finished.")

        return text_clf

    def save_model(self, text_clf, model="svm_abs_model.m"):
        joblib.dump(text_clf, model)

    def main(self, model="svm_abs_model.m"):
        text_clf = self.train()
        self.save_model(text_clf, model)


class Classify:
    def __init__(self, fmodel="svm_abs_model.m"):
        self.fmodel = fmodel
        assert os.path.exists(self.fmodel)
        self.model = joblib.load(self.fmodel)


    def build_data(self, x):
        x = list(map(lambda d: word_tokenize(clean_str(d)), x))
        return [" ".join(i) for i in x]

 
    def classify(self, txt):
        text = self.build_data([txt])
        preds = self.model.predict(text)
        return preds


if __name__ == "__main__":
    if not os.path.exists("model"):
        os.mkdir("model")
    SVM("abs").main("model/svm_abs_model.m")
    SVM("text").main("model/svm_text_model.m")
