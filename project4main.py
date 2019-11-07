# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 17:56:19 2019

@author: Peter
"""
import pandas as pd
import numpy as np
import porterstemmer
p = porterstemmer.PorterStemmer()

'''Method to turn a sentence string into a list of tokens'''
def tokenize (anArray):
    splitWordsArray = []
    for _ in range(0,len(sentences)):
        temp = []
        mystr = sentences[_].lower()
        for c in mystr[ : : 1]:
            if (not c.isalpha() and c != " "):
                mystr = mystr.replace(c,"")
            for x in nums:
                mystr = mystr.replace(x,"")       
            temp = mystr.split()
        splitWordsArray.append(temp)
    return splitWordsArray

'''Method to turn a list of tokens back to sentences, if needed (probably delete later)'''
def backToSentences (anArray):
    toReturn = []
    for aSentence in anArray:
        string = ""
        for aWord in aSentence:
            string = string + aWord + " "
        string = string[:-1]
        if(string):
            toReturn.append(string)
    return toReturn

'''Method to remove all stop words'''
def removeStopWords (anArray):
    toReturn = []
    for aSentence in anArray:
        tempSentence = aSentence
        for sw in stopwords:
            for aWord in tempSentence:
                if aWord == sw:
                    tempSentence.remove(aWord)
        if(tempSentence):
            toReturn.append(tempSentence)
    return toReturn

'''Method to use the Porter Stemmer algorithm provided to '''    
def portStem (anArray):
    toReturn = []
    for aSentence in anArray:
        tempSentence = aSentence
        sent = []
        for aWord in tempSentence:
            sent.append(p.stem(aWord,0,len(aWord)-1))
        toReturn.append(sent)
    return toReturn
    
'''Random Instantiated Items Here'''      
nums = ["0","1","2","3","4","5","6","7","8","9"]
thresh = 2

with open('stop_words.txt') as fp1:
    stopwords = fp1.read().splitlines()   #Maybe needs to be outside of open

sentences = []
with open('sentences.txt') as fp:
    line = fp.readline()
    while (line):
        sentences.append(line)
        line = fp.readline()
        
splitWords = tokenize(sentences)
noStopWords = removeStopWords(splitWords)
tokenPorterStemmed = portStem(noStopWords)
allWordsOrdered = []

for x in tokenPorterStemmed:
    for y in x:
        if not(y in allWordsOrdered):
            allWordsOrdered.append(str(y))
           
#initialize df
df = pd.DataFrame(0, index=range(1,len(tokenPorterStemmed)+1), columns = allWordsOrdered)

'''Creating the TDM from the init df object'''
for x in range(1, len(tokenPorterStemmed)+1):
    tempSent = tokenPorterStemmed[x-1]
    for y in tempSent:
        df[y].iat[x-1] = df[y].iat[x-1]+1
        
for x in range (1,len(tokenPorterStemmed)+1):
    sttemp = "Sentence " + str(x)
    df.rename(index={x : sttemp}, inplace=True)

dictionary = {}
for _ in df:
    dictionary[df[_].name] = df[_].sum()
dictionary = sorted(dictionary.items(), key = lambda kv: (kv[1], kv[0]))

for _ in df:
    if (df[_].sum() < thresh):
        df = df.drop(columns = [_])
df.to_csv('someName.csv', index=True)
print(df.columns)      
