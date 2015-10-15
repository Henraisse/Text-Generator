from random import randint
from TextModifier import TextModifier
import io
from NGMaker import NGMaker
from nltk.tag import pos_tag
from nltk import word_tokenize
import operator
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import sys



__author__ = 'Group 48'
#test stuff
class Main:
    global templetSentLS

    def findTemplet(self, corpusSents):
        "This function picks a random sentence from corpus, taggs it and returns a list of tags"

        sentNr = randint(0,(len(corpusSents)-1))
        sampleSent1 = corpusSents[sentNr]
        sampleSent  = sampleSent1.lower()

        tagged_sent = pos_tag(word_tokenize(sampleSent))

        pos_tags1 = [pos for (token,pos) in tagged_sent]
        #tokens1 = [token for (token,pos) in tagged_sent]

        #we stemm it, but also keep the original for grammar
        wnl = WordNetLemmatizer()
        sampleSentStemmed = [wnl.lemmatize(word) for word in word_tokenize(sampleSent)]

        #tag the sentence and leave only the tags left, this will be the template
        tagged_sent_lem = pos_tag(sampleSentStemmed)

        #return pos_tags
        print 'HERE IS THE TEMPLET', tagged_sent
        return tagged_sent_lem, tagged_sent

    def randomWordWithRightTag(self, taggedCorpus, tag):
        "If there is no word in the list of next usual words (bigram), we pick a word with right TAG"
        corpusLength = len(taggedCorpus)
        wordNr = randint(0,corpusLength-1)

        #wordTag1 = pos_tag(word_tokenize(TokanizedCorpus[wordNr]))
        corpusWordTuple = taggedCorpus[wordNr]
        corpusWordTag = corpusWordTuple[1]

        while corpusWordTag != tag: #or wordNr < (corpusLength-2):
            corpusWordTuple = taggedCorpus[wordNr]
            corpusWordTag = corpusWordTuple[1]
            wordNr = wordNr+1
            if wordNr >= (corpusLength-2):
                wordNr = randint(0,corpusLength-2)

        return corpusWordTuple

    def fillInTheInput(self, tag, templateSentLem, templateSent, corpusSents, taggedInput):
        notFound = True

        while notFound:
            i = 0
            for tupl in templateSentLem:
                if tag == tupl[1]:
                    templateSentLem[i] = taggedInput[0]
                    notFound = False
                    break
                i = i+1
            if notFound == True:
                templateSentLem, templateSent  = self.findTemplet(corpusSents)

        return templateSentLem, templateSent, i



    def buildSent(self, taggedCorpus, taggedInput, templateSentLem, templateSent, bigramc, trigram, i, j, bool):#tokenzc, word, tag_templet, bigram, trigram, i, j):
        "This function builds the right side of the sentence"
        #the place where we did put the input is i
        if bool == True:
            i = i+1
            #basecase, if the input is in the end of the template
            if i >= len(templateSentLem):
                return templateSentLem
        else:
            #the place where we did put the input is i
            i = i-1
            #basecase, if the input is in the end of the template
            if i <= -1:
                return templateSentLem

        tuple1 = templateSentLem[i]
        wordTag = tuple1[1]
        word1 = tuple1[0]
        nwlSameToken = []

        if word1 in stopwords.words('english'):
            return self.buildSent(taggedCorpus, taggedInput, templateSentLem, templateSent, bigramc, trigram, i, j, bool)
        else:
            if word1 in bigramc:
                nextWordList = bigramc[word1]

                #get the inner dictionary for the input word
                for w in nextWordList:
                    #print w, 'finns i listan'
                    if pos_tag(w[0]) == wordTag:
                        nwlSameToken.append(w)
            else:
                #todo, maybe we should handle this in some other way
                return self.buildSent(taggedCorpus, taggedInput, templateSentLem, templateSent, bigramc, trigram, i, j, bool)

        #if no words with the right Tag exist in the list of the words that use to follow
        if len(nwlSameToken) == 0:
            tag = wordTag
            mostProbWord = self.randomWordWithRightTag(taggedCorpus, wordTag)
            templateSentLem[i] = mostProbWord

            return self.buildSent(taggedCorpus, mostProbWord, templateSentLem, templateSent, bigramc, trigram, i, j, bool)

        #If there are words and we choose the most probable one
        else:
            sortedNextWordList = sorted(nextWordList.items(), key = operator.itemgetter(1))
            wordWithProb = sortedNextWordList[j]
            mostProbWordWithTag = pos_tag(wordWithProb[0])
            #the word is put in the telmpet
            templateSentLem[i] = mostProbWordWithTag
            #continue to the next word

            return self.buildSent(taggedCorpus, mostProbWordWithTag, templateSentLem, templateSent, bigramc, trigram, i, j, bool)

        return templateSentLem

def main():
    c = io.open('ourcorpus.txt', mode='r', encoding='utf-8')
    corpus = c.read()
    m = Main()


    tmc = TextModifier(corpus)

    #remove everything except words
    cleanedText = tmc.cleanText(corpus)
    #print(cleanedText), 'here is cleaned text'
    #make all lowercase
    lowercaseCorpus = [word.lower() for word in cleanedText]
    #remove all the stopwords from corpus
    noMoreStopwordsc = tmc.removeStopWords(lowercaseCorpus)
    #print(noMoreStopwordsc), 'here is no more stopWords'
    #lemetize
    lemmedCorpus = tmc.lemText(noMoreStopwordsc)
    #pos_tag()
    taggedCorpus = pos_tag(lemmedCorpus)
    #print(taggedCorpus)

    corpusSents = corpus.split('.')

    copyOfCorpus = lemmedCorpus[:]
    copyOfCorpus.reverse()
    bwCorpus = copyOfCorpus

    #make the bi and trigrams
    nm = NGMaker(lemmedCorpus)
    #unigram = nm._setugram(stemmedc)
    bigramc = nm._setBigram(lemmedCorpus)
    trigram = nm._setTrigram(lemmedCorpus)

    bigramBackW = nm._setBigram(bwCorpus)
    #trigramBackW = nm._setTrigram(lemmedCorpus.reverse())

    while True:
        #user input
        response = raw_input("\nPlease enter your input: ")
        tmr = TextModifier(response)

        templateSentLem, templateSent = m.findTemplet(corpusSents)

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
        #print(inputTag)


        print('Your input data is:')
        print(taggedInput)

        #put the input on the right place in the templet
        templateSentLem, templateSent, i = m.fillInTheInput(inputTag, templateSentLem, templateSent, corpusSents, taggedInput)
        print 'template sent with wirst word in it', templateSentLem


        #build the part of sentence that comes after the input word
        rightSent = m.buildSent(taggedCorpus, taggedInput, templateSentLem, templateSent, bigramc, trigram, i, -1, True)
        resultSent = m.buildSent(taggedCorpus, taggedInput, rightSent, templateSent, bigramBackW, trigram, i, -1, False)

        print 'The Result', resultSent
        for tuple in resultSent:
            sys.stdout.write(tuple[0])
            sys.stdout.write(" ")

if __name__ == '__main__':main()