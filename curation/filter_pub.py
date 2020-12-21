#!/usr/bin/env python3
"""Filter literature related to neoepitopes"""
import os
import shutil

def filter(path, out):
    if not os.path.exists(out):
        os.mkdir(out)

    idlist = set()
    for article in os.listdir(path):
        filename = os.path.join(path, article)
        text = open(filename).read()
        pmid = article.replace(".txt", "")
        if ((text.find("neo-epitopes") >= 0 and text.find("immune") >= 0)
            or (text.find("antigen") >= 0
            and text.find("T-cell") >= 0
            and text.find("immunotherapy") >= 0
            and text.find("lymphocytes") >= 0
            and text.find("melanoma") >= 0)):
            idlist.add(pmid)
        if ((text.find("mutated") >= 0 or text.find("mutation") >= 0)
            and text.find("tumor") >= 0
            and text.find("peptide") >= 0
            and text.find("HLA") >= 0):
            idlist.add(pmid)
        if text.find("T cell") >=0 and text.find("neoantigen") >= 0:
            idlist.add(pmid)

    for pmid in idlist:
        fname = "%s.txt" % pmid
        shutil.copyfile(os.path.join(path, fname), os.path.join(out, fname))

if __name__ == "__main__":
    filter("articles", "filtered")

