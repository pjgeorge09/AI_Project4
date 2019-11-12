# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 17:56:19 2019

@author: Peter
"""
import math
import pandas as pd
#This may need to be changed if you do not have porterstemmer imported locally
#It will be included in my zip folder
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

'''Method to print all euclidean distances in the dataset between points, for visualization'''
def printAllED (theDF):
    for x in range(0,len(theDF)):
        temp = theDF.iloc[x]
        ed1 = temp.values.tolist()
    for y in range (0,len(theDF)):
        temp2 = theDF.iloc[y]
        ed2 = temp2.values.tolist()
        print(ED(ed1,ed2))
        nums.append(ED(ed1,ed2))
    print("Max ED is " + str(max(nums)))
    print("Min ED is " + str(min(nums)))
    return

'''Method to calculate the Euclidean Distance between two datasets *Must be same length*'''
def ED(cluster1, cluster2):
    toReturn = math.sqrt(sum([(a-b)**2 for a,b in zip(cluster1,cluster2)]))
    return toReturn

'''Method to implement Forming Clusters As Needed (FCAN) algorithm
   on a set of data. Uses a dataframe object from Pandas.'''
def FCAN (theDF):
    
    dic = {}
    for x in range (1,len(theDF)+1): # Initialize dictionary of arrays
        dic[x] = []
    counter = 1 # Counter for the number of clusters total
    clusters = []
    cluster1 = theDF.iloc[0].values.tolist() # First Pattern is a cluster
    clusters.append(cluster1)
    dic[counter].append("Sentence 1") # Set first pattern as cluster and name it
    sentCounter = 1 # Sentence Counter. Marks the current sentence being worked on
    # For a sentence in the DF
    for x in range(1,len(theDF)):
        sentCounter += 1
        temp = theDF.iloc[x].values.tolist() # The Sentence
        clusterCounter = 0
        #Need to write condition where if it finds cluster, break loop stop looking
        foundACluster = False
        best = 10000 # The best case is the lowest Euclidean Distance
        # Find the best Euclidean Distance ahead of time, for ease.
        for _ in clusters:
            if(ED(_,temp) < EDmax and ED(_,temp) < best):
                best = ED(_,temp)
        # If there is a best Euclidean Distance that is sufficient, it will be added to that cluster
        for _ in clusters:
            clusterCounter += 1
            if(ED(_,temp) < EDmax and ED(_,temp) == best):
                #print("Sentence " + str(sentCounter) + " belongs to cluster " + str(clusterCounter))
                thing = "Sentence " + str(x+1)
                # Update the COG of the cluster this sentence is being added to
                clusters[(clusterCounter-1)] = update(clusters[(clusterCounter-1)], temp, dic[clusterCounter])
                dic[clusterCounter].append(thing)
                foundACluster = True
        # Done checking through all clusters, now IF DIDNT FIND ONE FAC should be False
        if(foundACluster == False):
            tempCluster = temp # This gonna be a new cluster
            clusters.append(tempCluster)
            counter += 1 # Update total number of clusters
            #print("Sentence " + str(sentCounter) + " creates to cluster " + str(counter))
            thing = "Sentence " + str(x+1) # Naming convention to match document provided
            dic[counter].append(thing)
            
    # Print out each cluster, and the sentences grouped therein        
    for _ in dic:
        if(dic[_]):
            print("Cluster " + str(_) + " has " + str(dic[_]))
    return

'''Method to update a cluster by adding a new setence, and updating the Center Of Gravity (COG)'''
def update (clusterWeights, newWeights, dicClusterSlice):
    for _ in range(0,len(clusterWeights)):
        clusterWeights[_] = (clusterWeights[_]*len(dicClusterSlice) + alpha * newWeights[_])/(len(dicClusterSlice)+1)
    return clusterWeights
  
'''--------------------------------MAIN STARTS HERE--------------------------'''
'''Random Instantiated Items Here'''      
nums = ["0","1","2","3","4","5","6","7","8","9"]
thresh = 4 #Minimum threshhold 3
alpha = 1 #Just doing COG
EDmax = 1.9 #Good alphas seem to be between 1.5 and 2.5

with open('stop_words.txt') as fp1:
    stopwords = fp1.read().splitlines()   #Maybe needs to be outside of open

sentences = []
with open('sentences.txt') as fp:
    line = fp.readline()
    while (line):
        sentences.append(line)
        line = fp.readline()

'''Tokenize. Remove Stop Words. Apply Porter Stemming.'''
splitWords = tokenize(sentences)    
noStopWords = removeStopWords(splitWords)
tokenPorterStemmed = portStem(noStopWords)

'''Order words if need be pre-pruning (Currently not used)'''
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
        
'''Giving the indexes appropriate names that match the Project 4 data sheet'''
for x in range (1,len(tokenPorterStemmed)+1):
    sttemp = "Sentence " + str(x)
    df.rename(index={x : sttemp}, inplace=True)

'''Sort all the words, if need be post-pruning (Currently not used)'''
dictionary = {}
for _ in df:
    dictionary[df[_].name] = df[_].sum()
dictionary = sorted(dictionary.items(), key = lambda kv: (kv[1], kv[0]))

'''Parse out columns that are irrelevant based on threshhold'''
for _ in df:
    if (df[_].sum() < thresh):
        df = df.drop(columns = [_])
df.to_csv('someName.csv', index=True)

'''Getting euclidean distances'''
#printAllED(df)

'''Does randomizing order make a difference? (Include line below to test this!)((ANS: YES!))'''      
#df = df.sample(frac=1)  
FCAN(df)