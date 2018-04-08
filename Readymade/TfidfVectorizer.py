import operator

import nltk
from django.db import connections
from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer

import glob

from Readymade.processingFile import Txt_generation_TF
from TFIDFVectorizer.settings import MEDIA_ROOT


def getDocList():
    list = glob.glob(MEDIA_ROOT + "\\documents\\allDocuments\\combo\\*.txt")
    return list


def getWords(request):
    def make_corpus(doc_files):
        corpus = []
        for doc in doc_files:
            f = open(doc)
            txt = ".".join(Txt_generation_TF(f, True))
            corpus.append(txt)

        # print(corpus)
        return corpus

    file_list = getDocList()
    LENGHT = len(file_list)
    print(file_list)
    corpus = make_corpus(file_list)

    vectorizer = TfidfVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus)
    # print(X)
    txt = []

    # database
    conn = connections['default']
    cursor = conn.cursor()

    for doc in range(0, LENGHT - 1):
        txt.append("------------------------doc " + file_list[doc] + "-------------------------------------")
        feature_index = X[doc, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])
        feature_names = vectorizer.get_feature_names()
        cur = {}
        for (i, s) in tfidf_scores:
            cur[feature_names[i]] = s
            query = "insert into t values (" + str(doc) + ",'" + feature_names[i] + "'," + str(s) + ")"
            print(query)
            cursor.execute(query)
        cur = sorted(cur.items(), key=operator.itemgetter(1), reverse=True)

        # print(cur)
        for w, s in cur:
            txt.append(w + " = " + str(s))
    return render(request, "myapp/display.html", {'data': txt})


# getWords()

# idf = vectorizer.idf_
# data=dict(zip(vectorizer.get_feature_names(), idf))
# txt=[]
# for k in data:
#     txt.append(k+" - "+ str(data[k]))

def search(request):
    if request.method == "POST":
        # database
        list=getDocList()
        conn = connections['default']
        cursor = conn.cursor()
        input = request.POST.get("input", "")
        input2=input
        doc=[]
        if input == "":
            return
        else:
            input = input.replace("?", "")
            keywords = input.split(" ")
            para = ""
            for key in keywords:
                para += "'" + key + "',"
            print(para)
            para = para[:len(para) - 1]
            print(para)
            query = "select doc_id,sum(tf_idf) from t where `key` IN(" + para + ") Group By (doc_id) Order By " \
                                                                                      "sum(tf_idf) desc "
            print(query)
            cursor.execute(query)
            for doc1 in cursor.fetchall():
                doc.append(list[doc1[0]])
        return render(request,"myapp/search.html",{"data":doc,"que":input2})
    return render(request, "myapp/search.html")