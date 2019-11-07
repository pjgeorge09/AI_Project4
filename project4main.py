# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 17:56:19 2019

@author: Peter
"""
import porterstemmer
p = porterstemmer.PorterStemmer()
with open('stop_words.txt') as fp1:
    stopwords = fp1.read().splitlines()   #Maybe needs to be outside of open

nums = ["0","1","2","3","4","5","6","7","8","9"]
sentences = []
with open('sentences.txt') as fp:
    line = fp.readline()
    while (line):
        sentences.append(line)
        line = fp.readline()
        
splitWords = []
for _ in range(0,len(sentences)):
    temp = []
    mystr = sentences[_].lower()
    for c in mystr[ : : 1]:
        if (not c.isalpha() and c != " "):
            mystr = mystr.replace(c,"")
    for x in nums:
        mystr = mystr.replace(x,"")       
    temp = mystr.split()
    splitWords.append(temp)
    
tempSentence = []
noStopWords = []
for aSentence in splitWords:
    tempSentence = aSentence
    for sw in stopwords:
        for aWord in tempSentence:
            if aWord == sw:
                tempSentence.remove(aWord)
    if(tempSentence):
        noStopWords.append(tempSentence)

backToStrings = []
for aSentence in noStopWords:
    string = ""
    for aWord in aSentence:
        string = string + aWord + " "
    string = string[:-1]
    if(string):
        backToStrings.append(string)
print(backToStrings)
st = "hellos"
sentence = p.stem(st,0,len(st)-1)
print(sentence)