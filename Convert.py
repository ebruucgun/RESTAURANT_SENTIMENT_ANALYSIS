import json
import pandas as pd
import re
import nltk
from regex import RegexReplacer
from nltk.corpus import stopwords
from PorterStemmer import *

stop = set(stopwords.words('english'))

rp = RegexReplacer() # Here the replaces is initialized.
p = PorterStemmer()#Here the porter stemmer is initialized.


#This function is used to use stemmer.
def stemm(line):
    line += " "
    line1 = ""
    element = ''
    for c in line:
        if c.isalpha():
            element += c.lower()
        else:
            if element:
                element = p.stem(element, 0,len(element)-1)
                line1 += element
                line1 += " "
                element = ''

    return line1


cuisines = ["American (Traditional)", "American (New)", "Latin American", "Italian", "Thai",
            "Chinese", "Japanese", "Turkish", "French", "Mexican", "German", "Polish", "Greek",
            "Pakistani", "Ethiopian", "Taiwanese", "Middle Eastern", "Indian", "Korean", "Vietnamese", "Canadian", ]
list = []
lines = open("yelp_academic_dataset_business.json",encoding='utf-8').readlines()
for line in lines:
    b_id = None
    cat = None
    name = None
    star = None
    cuis = "other"
    line_list = []
    jline = json.loads(line)
    for k, v in jline.items():
        if k == "categories":
            cat = v
        if k == "stars":
            star = v
        if k == "name":
            name = v
        if k=="business_id":
            b_id = v
    if(cat!= None):
        for cuisine in cuisines:
            if cuisine in cat:
                cuis = cuisine
                cat.remove(cuisine)
                break

    if (cat != None) and (name!=None):
        if ("restaurants" in cat) or ("Restaurants" in cat):
            if (star!= None) and (b_id != None):
                line_list.append(b_id)
                line_list.append(name)
                line_list.append(cat)
                line_list.append(star)
                list.append(line_list)

my_df = pd.DataFrame(list)
my_df.to_csv('business.csv', index=False, header=False)

list = []
lines1 = open("yelp_academic_dataset_review.json",encoding='utf-8').readlines()
for line in lines1:
    b_id = None
    text = None
    star = None
    line_list = []
    jline = json.loads(line)
    for k, v in jline.items():
        if k == "text":
            text = v
        if k == "stars":
            star = v
        if k=="business_id":
            b_id = v

    if text != None:
        if (star!= None) and (b_id != None):
            text = text.lower()
            text = rp.replace(text)
            text = re.sub("not ","not_",text)
            filtered_words = ""
            for i in text.split():
                if i not in stop:
                    filtered_words+=i
                    filtered_words+=" "
            text = stemm(filtered_words)
            line_list.append(b_id)
            line_list.append(text)
            line_list.append(star)
            list.append(line_list)

my_df1 = pd.DataFrame(list)
my_df1.to_csv('review.csv', index=False, header=False)
