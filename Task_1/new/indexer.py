from genericpath import isfile
import os
import json


def InvertedIndex():
    publications = None
    if os.path.isfile(os.path.join("data.json")):
        with open(os.path.join("data.json"),"r") as jsonFile:
            publications = json.load(jsonFile)
    else:
        return publications
    
    invertedIndex = dict()
    for id_, article in publications.items():
        for key in article["filtered_title"]:
            if key not in invertedIndex:
                invertedIndex[key] = dict()
            invertedIndex[key][id_] = True
    return invertedIndex
