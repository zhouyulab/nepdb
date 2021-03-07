import os
import shutil
from trainSVM import Classify


total = set(list(i.replace(".txt", "") for i in os.listdir("abstracts")))
pos = set(list(i.replace(".txt", "") for i in os.listdir("data/pos_abstract")))

print(f"total: {len(total)}")
print(f"total & pos: {len(total & pos)}")

abs_model = Classify("model/svm_abs_model.m")

abs_filter = []

if not os.path.exists("abs_filter"):
    os.mkdir("abs_filter")

for pmid in total:
    text = open(os.path.join("abstracts", pmid+".txt")).read()
    if abs_model.classify(text) == 1:
        abs_filter.append(pmid)
        shutil.copy(os.path.join("abstracts", pmid+".txt"), os.path.join("abs_filter", pmid+".txt"))

print(f"abs_filter: {len(abs_filter)}")
print(f"abs_filter & pos: {len(set(abs_filter) & pos)}")
