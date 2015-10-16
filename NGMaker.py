from __future__ import division
from nltk.util import ngrams
from nltk.probability import FreqDist, SimpleGoodTuringProbDist

class NGMaker():


    def __init__( self, listInput ):
        self.text = listInput

    #TODO
    def _setugram(self, listInput):
        self._uniGram = listInput

        freqList = self._setuFdist()

        return freqList

    def _setBigram(self, listInput):

        bigramList = ngrams(listInput, 2)
        bigramFreq = self.countProbability(bigramList)
        outerBigram = {}
        size = len(listInput)

        sgtBig = SimpleGoodTuringProbDist(bigramFreq)

        for bigram in bigramFreq:
            b = bigram[0]
            if b in outerBigram :
                innerBigram1 = outerBigram[b]
                innerBigram1[bigram[1]] = (sgtBig.prob(bigram))
            else:
                innerBigram = {}
                innerBigram[bigram[1]] = (sgtBig.prob(bigram))
                outerBigram[b] = innerBigram
        return outerBigram

    def _setTrigram(self, listInput):
        trigramList = ngrams(listInput,3)
        trigramFreq = self.countProbability(trigramList)
        outerTrigram = {}
        size = len(listInput)

        sgtTri = SimpleGoodTuringProbDist(trigramFreq)

        for trigram in trigramFreq:
            b = trigram[0:2]
            if b in outerTrigram:
                innerTrigram = outerTrigram[b]
                innerTrigram[trigram[2]] = (sgtTri.prob(trigram))
            else:
                innerTrigram = {}
                innerTrigram[trigram[2]] = (sgtTri.prob(trigram))
                outerTrigram[b] = innerTrigram

        return outerTrigram


    #the function that calls for dist and prob of unigram.
    def _setuFdist(self):
        self._uniFdist = self.countProbability(self._uniGram)
        return self.makeAProbMapUgram()

    def makeBigramTree(self, listInput):
        bigram = self.makeBigram(listInput)

    #A list vith tuples (word, nr.of occ)
    def countProbability(self, ngram):
        fdist = FreqDist(ngram)
        return fdist

    #makes a dictionary with {word:probability, squirrel:0.343444}
    def makeAProbMapUgram(self):
        map = {}
        size = len(self._uniFdist)
        for j,v in self._uniFdist.items():
            map[j] = float(v/size)
        return map



