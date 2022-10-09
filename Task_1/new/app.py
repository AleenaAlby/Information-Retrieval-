from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from indexer import InvertedIndex
import re
import os
import json

app = Flask(__name__)
searchIndex = None
data = None

#IndexPage
@app.route('/', methods=["POST", "GET"])
def index():
    searchQuery = ""
    article = None
    if request.method == "POST":
        searchQuery = request.form['searchWord']
        article = filterArticle(searchQuery)
    return render_template('index.html', articles_ = article, searchWord = searchQuery )

def loadData():
    with open(os.path.join("data.json"), "r") as read_file:
        data = json.load(read_file)
    invertedIndex = InvertedIndex()
    return data, invertedIndex
    

def filterArticle(searchQuery):
    result = []
    relevance = dict()
    searchQuery = [
        word
        for word in word_tokenize(
            re.sub("\W+"," ", searchQuery.lower().strip())
        )
        if not word in set(stopwords.words("english"))
    ]

    for word in searchQuery:
        for pubId in searchIndex.get(word, list()):
            relevance[pubId] = relevance.get(pubId,0) + 1 

    relevance = sorted(relevance.items(), key = lambda rank: rank[1], reverse=True)
    result = [data[pubId] for pubId, _ in relevance]

    return result



if __name__ == '__main__':
    data, searchIndex = loadData()
    app.run(debug=True)

