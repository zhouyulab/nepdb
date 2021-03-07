import os
import shutil
from trainSVM import Classify

abs_filter = set(list(i.replace(".txt", "") for i in os.listdir("abs_filter")))
pos = set(list(i.replace(".txt", "") for i in os.listdir("data/pos_abstract")))

text_model = Classify("model/svm_text_model.m")
text_filter = []

if not os.path.exists("text_filter"):
    os.mkdir("text_filter")

for pmid in abs_filter:
    path = os.path.join("fulltext", pmid+".txt")
    if not os.path.exists(path):
        continue
    text = open(path).read()
    if text_model.classify(text) == 1:
        text_filter.append(pmid)

    shutil.copy(path, os.path.join("text_filter", pmid+".txt"))

print("text_filter: ", len(text_filter))
print("text_filter & pos: ", len(set(text_filter) & pos))