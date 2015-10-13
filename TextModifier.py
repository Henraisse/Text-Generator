__author__ = 'Group 48'
from nltk import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk.data

class TextModifier():

    def __init__( self, textInput ):
        text = textInput


    def cleanText( self, text ):
        "This function remones punctuation from text input"
        tokenizer = RegexpTokenizer(r'\w+')
        tokenz = tokenizer.tokenize(text)

        return tokenz

    def stemmText(self, textInputs):
        #Lematisation of the data using porter stemmer algorithm
        #http://tartarus.org/martin/PorterStemmer/
        #there exist other algorithms such as
        # http://www.comp.lancs.ac.uk/computing/research/stemming/
        # http://snowball.tartarus.org/

        porter_stemmer = PorterStemmer()
        stemmedText = [porter_stemmer.stem(textInput) for textInput in textInputs]
        return stemmedText
    def removeStopWords(self, textInputs):
        filtered_words = [word for word in textInputs if word not in stopwords.words('english')]
        return filtered_words

    def lowercase(self, textInput):
        low = [word.lower() for word in textInput]
        return low