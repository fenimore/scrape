"""
    Some Python Text Analysis
    Do not Run this program, copy the appropriate tests
    to something like ipython Notebook.
"""

"""Clean up and Loop documents"""
import os
import nltk
import glob
import matplotlib.pyplot as plt
import re
from os import listdir
from bs4 import BeautifulSoup
from textblob import TextBlob
 
# this is the function to string xml tags from files
# beautiful soup will parse the xml
def strip_tags(textFile):
    soup = BeautifulSoup(open(textFile), "lxml")
    stripped_text = soup.get_text()
    return stripped_text

# loop through the files using glob
textFiles = glob.glob("*.xml")
# and run it:
for textFile in textFiles:
    #output = [perform operation on THIS textFile]
    #print output
    
"""Collocations"""
i = 0
for textFile in textFiles:
    cleanText = strip_tags(textFile)
    textTokens = nltk.word_tokenize(cleanText.lower()) # tokenize
    textWords = [word for word in textTokens if any([c for c in word if c.isalpha()])] #get words
    textText = nltk.Text(textWords) #get nltk Text 
    textText.collocations(5)
    print i, textFile
    i += 1

"""NLTK Tokenize"""
cleanText = strip_tags(textFile) #or for a single file "textFiles[x]"
corpus.append(cleanText) #gather into one variable this takes a while
textTokens = nltk.word_tokenize(cleanText.lower()) # tokenize
textWords = [word for word in textTokens if any([c for c in word if c.isalpha()])] #get words
textText = nltk.Text(textWords) #get nltk Text


"""TextBlob"""
#Polarity Score
i = 0
for textFile in textFiles:
    cleanText = strip_tags(textFile)
    blob = TextBlob(cleanText)
    print i, ": ", blob.sentiment.polarity, " in ", textFile
    i += 1

# For Single File
cleanText = strip_tags(textFiles[136])
blob = TextBlob(cleanText)
print blob.sentiment.polarity

"""Bigrams Matplot Implementation"""
# This goes within the Loop of cleaned documents:

    bigraming = list(nltk.ngrams(textWords, 2))
    gramFreq = nltk.FreqDist(bigraming)
    for words, count in gramFreq.most_common(3):
        print(count, " ".join(list(words)))
 
    %matplotlib inline
    textText.dispersion_plot(["god"])
    bigraming = list(nltk.ngrams(textWords, 2))
    gramFreq = nltk.FreqDist(bigraming)
    for words, count in gramFreq.most_common(3):
        print(count, " ".join(list(words)))
