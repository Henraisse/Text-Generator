from random import randint
from TextModifier import TextModifier
import io
from NGMaker import NGMaker
from nltk.tag import pos_tag
from nltk import word_tokenize
import operator
from nltk.stem import WordNetLemmatizer


__author__ = 'Group 48'
#test stuff
class Main:

    def findTemplet(self, corpusSents):
        "This function picks a random sentence from corpus, taggs it and returns a list of tags"

        sentNr = randint(0,(len(corpusSents)-1))
        sampleSent = corpusSents[sentNr]
        tagged_sent = pos_tag(word_tokenize(sampleSent))

        pos_tags1 = [pos for (token,pos) in tagged_sent]
        #tokens1 = [token for (token,pos) in tagged_sent]

        #we stemm it, but also keep the original for grammar
        wnl = WordNetLemmatizer()
        sampleSentStemmed = [wnl.lemmatize(word) for word in sampleSent.split()]

        #tag the sentence and leave only the tags left, this will be the template
        tagged_sent = pos_tag(sampleSentStemmed)
        pos_tags = [pos for (token,pos) in tagged_sent]
        #tokens = [token for (token,pos) in tagged_sent]

        return pos_tags

    def randomWordWithRightTag(self, TokanizedCorpus, tag):
        "If there is no word in the list of next usual words (bigram), we pick a word with right TAG"
        corpusLength = len(TokanizedCorpus)
        wordNr = randint(0,corpusLength-1)

        wordTag1 = pos_tag(word_tokenize(TokanizedCorpus[wordNr]))
        print(wordTag1)
        wordTag2 = wordTag1[0]
        print(wordTag2)
        wordTag = wordTag2[1]
        #print(wordTag)
        #print wordTag
        while wordTag != tag: #or wordNr < (corpusLength-2):
            print wordNr
            print tag
            print wordTag

            wordTag1 = pos_tag(word_tokenize(TokanizedCorpus[wordNr]))
            wordTag2 = wordTag1[0]
            wordTag = wordTag2[1]
            wordNr = wordNr+1
            if wordNr == (corpusLength-2):
                wordNr = randint(0,corpusLength-2)

            #print(wordTag)

        return wordTag2

    def buildRight(self, tokenzc, word, tag_templet, bigram, trigram, i, j):
        "This function builds the right side of the sentence"
        #the place where we did put the input is i
        i = i+1
        #basecase, if the input is in the end of the template
        if i == len(tag_templet):
            return tag_templet

        wordTag = tag_templet[i]
        #TODO this is just for now and does not seem to work
        if wordTag in {'TO', 'WP','-NONE-','WDT','CC'}:
            self.buildRight(tokenzc, word, tag_templet, bigram, trigram, i, j)
        #get the inner dictionary for the input word
        #TODO i think that this never happens, i donno
        nextWordList = bigram[word]
        nwlSameToken = []
        for w in nextWordList:
            if pos_tag(word_tokenize(w[0])) == wordTag:
                nwlSameToken.append(word)
                print(nwlSameToken)

        #if no words with the right Tag exist in the list of the words that use to follow
        if len(nwlSameToken) == 0:
            tag = wordTag
            mostProbWord = self.randomWordWithRightTag(tokenzc, tag)
            tag_templet[i] = mostProbWord
            print mostProbWord[0]
            self.buildRight(tokenzc, mostProbWord[0], tag_templet, bigram, trigram, i, -1)
            print(tag_templet)
        #If there are words and we choose the most probable one
        else:
            sortedNextWordList = sorted(nextWordList.items(), key = operator.itemgetter(1))
            #tag the word and see if it is right
            mostProbWordWithTag = sortedNextWordList[j]
            #the word is put in the telmpet
            tag_templet[i] = mostProbWordWithTag
            #continue to the next word
            self.buildRight(tokenzc, mostProbWordWithTag, tag_templet, bigram, trigram, i, -1)

        return tag_templet


    def fillInTheInput(self, inputTag, templateSent, corpusSents, stemmedInput):
        notFound = True
        while notFound:
            i = 0
            for tag in templateSent:
                if tag == inputTag:
                    templateSent[i] = stemmedInput[0]
                    notFound = False
                    break
                i = i+1
            if notFound == True:
                templateSent = m.findTemplet(corpusSents)

        print(templateSent)
        return templateSent, i



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


    tmc = TextModifier(corpus)

    #remove everything except words
    cleanedText = tmc.cleanText(corpus)
    #make all lowercase
    lowercaseCorpus = [word.lower() for word in cleanedText]
    #remove all the stopwords from corpus
    noMoreStopwordsc = tmc.removeStopWords(lowercaseCorpus)
    #lemetize
    LemmedCorpus = tmc.lemText(noMoreStopwordsc)
    #pos_tag()


    #split the corpus on sentences
    #corpusSents = corpus.sent()
    #TODO we should probably send a tagged corpus here, then we wont have to tag words forever
    corpusSents = corpus.split('.')
    templateSent = m.findTemplet(corpusSents)


    #user input
    response = raw_input("Please enter your input: ")
    tmr = TextModifier(response)
    #remove everything except words
    cleanInput = tmr.cleanText(response)
    #all chars to lowercase
    lowercaseInput = [word.lower() for word in cleanInput]
    #remove stop words
    noStopwordsInput = tmr.removeStopWords(lowercaseInput)
    #Stemming
    stemmedInput = tmr.lemText(noStopwordsInput)

    #tag response IF one word
    #IF many words this has to be done as pos_tags = [pos for (token,pos) in tagged_sent]
    taggedInput = pos_tag(word_tokenize(stemmedInput[0]))
    #clean the input

    dummyTag = taggedInput[0]
    inputTag = dummyTag[1]
    print(inputTag)

    #make the bi and trigrams
    nm = NGMaker(LemmedCorpus)
    #unigram = nm._setugram(stemmedc)
    bigramc = nm._setBigram(LemmedCorpus)
    trigram = nm._setTrigram(LemmedCorpus)

    print('Your input data is:')
    print(stemmedInput)

    #put the input on the right place in the templet
    templateSent, i = m.fillInTheInput(inputTag, templateSent, corpusSents, stemmedInput)



    #build the part of sentence that comes after the input word
    rightSent = m.buildRight(LemmedCorpus, stemmedInput[0], templateSent, bigramc, trigram, i, -1)

    print rightSent


if __name__ == '__main__':main()