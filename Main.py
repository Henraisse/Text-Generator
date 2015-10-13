from random import randint
from TextModifier import TextModifier
import io
from NGMaker import NGMaker
from nltk.corpus import brown
from nltk.tag import pos_tag
from nltk.parse import RecursiveDescentParser
from nltk import word_tokenize
import operator


__author__ = 'Group 48'
#test stuff
class Main:

    def findTemplet(self, corpusSents):
        #choose one of the sentences randomly
        sentNr = randint(0,len(corpusSents))
        sampleSent = corpusSents[sentNr]

        #tag the sentence and leave only the tags left, this will be the template
        tagged_sent = pos_tag(sampleSent.split())
        pos_tags = [pos for (token,pos) in tagged_sent]
        tokens = [token for (token,pos) in tagged_sent]
        print(tokens)
        print(pos_tags)
        return pos_tags

    def buildRight(self, stemmed, pos_tags, bigram, trigram):

        nextWordList = bigram[stemmed[0]]
        sortedNextWordList = sorted(nextWordList.items(), key = operator.itemgetter(1))
        print(sortedNextWordList)

        #ga igenom listan och hitta forst den med hogst sannolikhet
        #och ratt tag
        #annars kolla genom resten
        #annars ta ett random ord med ratt tag
        #satt in funnet ord i pos tag
        #anropa en funktion som fixar grejer med trigram, den ska fylla pa resten
        #misslyckas den sa ska den ner till bigram
        # sen ska vi fixa vanster sida av meningen med hjalp av Jennys grejer


def main():
    c = io.open('ourcorpus.txt', mode='r', encoding='utf-8')
    corpus = c.read()
    m = Main()
    #corpus = brown.words()
    ##print(corpus)
    # proccess corpus
    tmc = TextModifier(corpus)
    tokenzc = tmc.cleanText(corpus)
    lowercaseListc = tmc.lowercase(tokenzc)
    noMoreStopwordsc = tmc.removeStopWords(lowercaseListc)
    stemmedc = tmc.stemmText(noMoreStopwordsc)


    #split the corpus om sentences
    #corpusSents = corpus.sent()
    corpusSents = corpus.split('.')
    pos_tags = m.findTemplet(corpusSents)


    #take user input
    response = raw_input("Please enter your input: ")
    tmr = TextModifier(response)
    tokenz = tmr.cleanText(response)
    #all chars to lowercase
    lowercaseList = tmr.lowercase(tokenz)
    #remove stop words
    noMoreStopwords = tmr.removeStopWords(lowercaseList)
    #Stemming
    stemmed = tmr.stemmText(noMoreStopwords)

    #tag response IF one word
    #IF many words this has to be done as pos_tags = [pos for (token,pos) in tagged_sent]
    responseAndTag = pos_tag(word_tokenize(stemmed[0]))
    #clean the input

    dummyTag = responseAndTag[0]
    inputTag = dummyTag[1]
    print(inputTag)

    #make the bi and trigrams
    nm = NGMaker(stemmedc)
    unigram = nm._setugram(stemmedc)
    bigramc = nm._setBigram(stemmedc)
    trigram = nm._setTrigram(stemmedc)

    print('Your input data is:')
    print(stemmed)

    #put the input on the right place in the templet
    notFound = True
    while notFound:
        i = 0
        for tag in pos_tags:
            if tag == inputTag:
                pos_tags[i] = stemmed[0]
                notFound = False
                break
            i = i+1
        if notFound == True:
            pos_tags = m.findTemplet(corpusSents)

    print(pos_tags)

    #build the part of sentence that comes after the input word
    rightSent = m.buildRight(stemmed, pos_tags, bigramc, trigram)

    sent = ''
    _tmp = []

if __name__ == '__main__':main()