import json
import numpy as np
#### please install 2 library before using ####
###### pip install fuzzywuzzy
###### pip install python-Levenshtein
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

###### Dictionary for Matching ######
with open("../dataset/SearchIPA.json", encoding="utf8") as f:
        search_ipa_dict = json.loads(f.read())

with open("../dataset/ENG2IPA.json", encoding="utf8") as f:
        eng2ipa_dict = json.loads(f.read())

def IPA_matching(ipa):
    """
    function for matching input ipa(string) with eng word in dictionary by using fuzzy matching method
    return eng_word, and similarity score of input ipa and ipa of output word
    """
    res = process.extract(ipa, search_ipa_dict, scorer=fuzz.ratio,limit=1)
    similarity_score = res[0][1]
    return res[0][2], similarity_score/100

def ENG2IPA(eng):
    """
    function for use dictionary to convert eng word to ipa (for using in evaluate)
    """
    return eng2ipa_dict[eng]

def evaluate_matching(x,y):
    """
    function for evaluate matching method with x is ipa and y is the ground truth eng words and it will output accuracy and list of wrong predict words and list of true words
    """
    pred = []
    for i in x:
        res,_ = IPA_matching(i)
        pred.append(res)
    pred = np.array(pred)
    y = np.array(y)
    res = (pred==y)
    acc = (np.sum(res))/len(res)
    res = ~res
    true_words = y[res]
    wrong_words = pred[res]
    return acc, wrong_words.tolist(), true_words.tolist()