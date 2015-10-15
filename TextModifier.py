__author__ = 'Group 48'
from nltk import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

class TextModifier():

    def __init__( self, textInput ):
        text = textInput


    def cleanText( self, text ):
        "This function remones punctuation from text input"
        tokenizer = RegexpTokenizer(r'\w+')

        tokenz = tokenizer.tokenize(text)

        return tokenz
        #return text2

    def lemText(self, textInputs):
        #Lematisation of the data using WordNetLemmatizer algorithm
        #http://tartarus.org/martin/PorterStemmer/
        #there exist other algorithms such as
        # http://www.comp.lancs.ac.uk/computing/research/stemming/
        # http://snowball.tartarus.org/

        wnl = WordNetLemmatizer()
        stemmedText = [wnl.lemmatize(textInput) for textInput in textInputs]
        return stemmedText
    def removeStopWords(self, textInputs):
        filtered_words = [word for word in textInputs if word not in stopwords.words('english')]
        return filtered_words

    #def lowercase(self, textInput):
        #low = [word.lower() for word in textInput]
        #return low