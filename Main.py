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
        print 'HERE IS THE TEMPLET', tagged_sent_lem
        return tagged_sent_lem, tagged_sent

    def randomWordWithRightTag(self, taggedCorpus, tag, tup, bigram):
        "If there is no word in the list of next usual words (bigram), we pick a word with right TAG"
        if tup[0] not in bigram:
            return tup
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



    def buildSent(self, taggedCorpus, taggedInput, templateSentLem, bigramc, i, j, bool):#tokenzc, word, tag_templet, bigram, trigram, i, j):
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
        word1 = taggedInput[0]
        nwlSameToken = []

        if word1 not in bigramc: #stopwords.words('english'):
            return self.buildSent(taggedCorpus, taggedInput, templateSentLem, bigramc, i, j, bool)
        else:
            if word1 in bigramc:
                nextWordList = bigramc[word1]

                #get the inner dictionary for the input word
                for w in nextWordList:
                    #print w, 'finns i listan'
                    if pos_tag(w[0]) == wordTag:
                        nwlSameToken.append(w)
            else:
                #todo, This should never happen, all theh words from input are in corpus
                return self.buildSent(taggedCorpus, taggedInput, templateSentLem, bigramc, i, j, bool)

        #if no words with the right Tag exist in the list of the words that use to follow
        if len(nwlSameToken) == 0:
            tag = wordTag
            print('in i random')
            mostProbWord = self.randomWordWithRightTag(taggedCorpus, wordTag,templateSentLem[i], bigramc)
            print('ut ur random')
            templateSentLem[i] = mostProbWord

            return self.buildSent(taggedCorpus, mostProbWord, templateSentLem, bigramc, i, j, bool)

        #If there are words and we choose the most probable one
        else:
            sortedNextWordList = sorted(nextWordList.items(), key = operator.itemgetter(1))
            wordWithProb = sortedNextWordList[j]
            mostProbWordWithTag = pos_tag(wordWithProb[0])
            #the word is put in the telmpet
            templateSentLem[i] = mostProbWordWithTag
            #continue to the next word

            return self.buildSent(taggedCorpus, mostProbWordWithTag, templateSentLem, bigramc, i, j, bool)

        return templateSentLem


    def buildSentTri(self, taggedCorpus, taggedTuple, templateSentLem, bigramc, trigram, i, j, first,rl):

        i = i+1
        #basecase, if the input is in the end of the template
        if i >= len(templateSentLem):
            return templateSentLem

        #print 'i bygg hoger', thisElem, nextElem

        if first == True:
            thisElem = templateSentLem[i-1]
            nextElem = templateSentLem[i]
            listToSend = [thisElem,nextElem]
            m = 1
            while nextElem[0] not in bigramc and (m+i)<len(templateSentLem):#in stopwords.words('english') and (m+i)<len(templateSentLem):
                nextElem = templateSentLem[i+m]
                listToSend.append(nextElem)
                m = m+1
            print thisElem, 'thisELement'
            print listToSend, 'list to send'
            print(m)
            putThisBack = self.buildSent(taggedCorpus, thisElem, listToSend, bigramc, m-1, j, rl)
            n = 0
            print 'put this back ', putThisBack
            for a in putThisBack:
                templateSentLem[i+n-1] = a
                n = n+1
            print 'efter bi gram', templateSentLem
            taggedTuple = [thisElem,putThisBack[-1]]
            return self.buildSentTri(taggedCorpus, taggedTuple, templateSentLem, bigramc, trigram, i+n-2, j, False, rl)

        #if templateSentLem[i] in stopwords.words('english'):
        print 'jag kan false'
        d = templateSentLem[i-1]
        if d[0] not in bigramc:
            print d[0], 'finns inte i bigram'
            return self.buildSentTri(taggedCorpus,taggedTuple , templateSentLem, bigramc, trigram, i, j, False, rl)

        else:
            t1 = taggedTuple[0]
            t2 = taggedTuple[1]
            tup = (t1[0],t2[0])
            print tup, 'kollar om den har efterfoljare'
            nwlSameToken = []
        if tup in trigram:
            print 'JAG AR HAR!!!'
            nextWordList = trigram[tup]
            #get the inner dictionary for the input word
            for w in nextWordList:
                #print w, 'finns i listan'
                g = templateSentLem[i]
                if pos_tag(w[0]) == g[1]:
                    nwlSameToken.append(w)
            print 'alla efterfoljare', nwlSameToken
        else:
            #todo, This should never happen, all theh words from input are in corpus
            return self.buildSentTri(taggedCorpus,taggedTuple[1], templateSentLem, bigramc, trigram, i-1, j, True,rl)

        if len(nwlSameToken) == 0:
            return self.buildSentTri(taggedCorpus, taggedTuple[1], templateSentLem, bigramc, trigram, i-1, j, True,rl)

        #If there are words and we choose the most probable one
        else:
            sortedNextWordList = sorted(nextWordList.items(), key = operator.itemgetter(1))
            wordWithProb = sortedNextWordList[j]
            mostProbWordWithTag = pos_tag(wordWithProb[0])
            #the word is put in the telmpet
            templateSentLem[i] = mostProbWordWithTag
            #continue to the next word

            return self.buildSentTri(taggedCorpus,[taggedTuple[1],templateSentLem[i]] , templateSentLem, bigramc, trigram, i, j, False,rl)

        return templateSentLem



    def buildSentTriLeft(self, taggedCorpus, taggedTuple, templateSentLem, bigramBackW, trigramBackW, i, j, first, rl):

        #the place where we did put the input is i
        i = i-1
        #basecase, if the input is in the end of the template
        if i <= -1:
            print(templateSentLem)
            return templateSentLem


        #The first time we entered with just user input
        if first == True:
            thisElem = templateSentLem[i+1]
            nextElem = templateSentLem[i]

            listToSend = [nextElem, thisElem]
            m = 1
            while nextElem[0] not in bigramBackW and (i-m)>=0:
                print 'jag ar stopord eller nat'
                listToSend = [templateSentLem[i-m]]+ listToSend
                nextElem = templateSentLem[i-m]
                m = m+1
            print 'nu skickar jag till bigram', listToSend
            putThisBack = self.buildSent(taggedCorpus, thisElem, listToSend, bigramBackW, 1, j, rl)
            n = 0
            print 'put this back ', putThisBack
            for a in putThisBack:
                templateSentLem[i-m+n+1] = a
                n = n+1
            print 'efter bi gram', templateSentLem
            taggedTuple = [thisElem,putThisBack[-1]]
            return self.buildSentTriLeft(taggedCorpus,taggedTuple , templateSentLem, bigramBackW, trigramBackW, i-n+2, j, False, rl)


        wordTupBefTuple = templateSentLem[i]
        if wordTupBefTuple[0] not in bigramBackW:#stopwords.words('english'):
            print 'not in bigram'
            return self.buildSentTriLeft(taggedCorpus, taggedTuple , templateSentLem, bigramBackW, trigramBackW, i, j, False, rl)

        else:
            print 'finns i bigram'
            t1 = taggedTuple[0]
            t2 = taggedTuple[1]
            tup = (t1[0],t2[0])
            nwlSameToken = []
        if tup in trigramBackW:
            print 'JAG AR HAR!!!22222'
            nextWordList = trigramBackW[tup]

            #get the inner dictionary for the input word
            for w in nextWordList:
                print 'JAg kollar i next word list'
                #print w, 'finns i listan'
                g = templateSentLem[i]
                if pos_tag(w[0]) == g[1]:
                    nwlSameToken.append(w)
        else:
            #If tuple does not exist go to trigram but make it look for bigram
            return self.buildSentTriLeft(taggedCorpus, taggedTuple[1] , templateSentLem, bigramBackW, trigramBackW, i+1, j, True, rl)

        if len(nwlSameToken) == 0:
            print 'jag har inga efterfoljare'
            return self.buildSentTriLeft(taggedCorpus, taggedTuple[1], templateSentLem, bigramBackW, trigramBackW, i+1, j, True, rl)

        #If there are words and we choose the most probable one
        else:
            sortedNextWordList = sorted(nwlSameToken.items(), key = operator.itemgetter(1))
            wordWithProb = sortedNextWordList[j]
            mostProbWordWithTag = pos_tag(wordWithProb[0])
            #the word is put in the telmpet
            templateSentLem[i] = mostProbWordWithTag
            #continue to the next word

            return self.buildSentTriLeft(taggedCorpus,[taggedTuple[1],templateSentLem[i]] , templateSentLem, bigramBackW, trigramBackW, i, j, False, rl)

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
    unigram = nm._setugram(lemmedCorpus)
    bigramc = nm._setBigram(lemmedCorpus)
    trigram = nm._setTrigram(lemmedCorpus)

    bigramBackW = nm._setBigram(bwCorpus)
    trigramBackW = nm._setTrigram(bwCorpus)
    #print taggedCorpus
    #t = (u'getting', u'day')
    #print (trigram[(u'blame', u'ta')])

    while True:
        #user input
        a = True

        response = raw_input("\nPlease enter your input: ")
        tmr = TextModifier(response)

        #remove everything except words
        cleanInput = tmr.cleanText(response)
        #all chars to lowercase
        lowercaseInput = [word.lower() for word in cleanInput]
        #remove stop words
        noStopwordsInput = tmr.removeStopWords(lowercaseInput)
        #Stemming
        stemmedInput = tmr.lemText(noStopwordsInput)

        print(stemmedInput)
        if stemmedInput[0] in bigramc:
            a = False
        if a == True:
            print 'This is not a word that exist in corpus'
        if not a:
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
            #rightSent = m.buildSent(taggedCorpus, taggedInput, templateSentLem, bigramc, i, -1, True)
            #resultSent = m.buildSent(taggedCorpus, taggedInput, rightSent, bigramBackW, i, -1, False)

            resultTriGram = m.buildSentTri(taggedCorpus, taggedInput, templateSentLem, bigramc, trigram, i, -1, True , True)
            resultTriGram = m.buildSentTriLeft(taggedCorpus, taggedInput, resultTriGram, bigramBackW, trigramBackW, i, -1, True, False) #TODO KO IHaG MIG


            print 'Templet', templateSent#resultSent
            for tuple in templateSent:#resultSent:
                sys.stdout.write(tuple[0])
                sys.stdout.write(" ")

            print '\nThe Result', resultTriGram#resultSent
            for tuple in resultTriGram:#resultSent:
                sys.stdout.write(tuple[0])
                sys.stdout.write(" ")



if __name__ == '__main__':main()