import sys
import math
from collections import Counter

occurrences = []
words = []
total_words = 0

feats_file = sys.argv[1]
data_file = sys.argv[2]

# read feats file
with open(feats_file) as f:
	text = f.read()

# read data file
with open(data_file) as f:
	text2 = f.read()

lines = text.split('\n')
lines2 = text2.split('\n')

#wordPosLemmaConcept = []
wordConcept = []
words = []
lemmas = []
pos = []
concept = [] 
counterWords = 0
counterLemmaPos = {}
counterLemmaPosConcept = {}

#wordsRepetitions = []

for line, line2 in zip(lines, lines2):
	line = line.strip()
	line2 = line2.strip()
	if not line: continue
	counterWords = counterWords+1
	parts = line.split('\t')
	parts2 = line2.split('\t')
	#wordPosLemmaConcept.append(parts[0]+"\t"+parts[1]+"\t"+parts[2]+"\t"+parts2[1])
	wordConcept.append(parts[0]+"\t"+parts2[1])
	words.append(parts[0])
	#lemmas.append(parts[2])
	#pos.append(parts[1])
	concept.append(parts2[1])
	#wordsRepetitions.append(parts[0])
	#wordsRepetitions.append(parts2[1])

#counterWordPosLemmaConcept = Counter(wordPosLemmaConcept).most_common()
counterWordConcept = Counter(wordConcept).most_common()
counterWord = dict(Counter(words))
#counterLemma = dict(Counter(lemmas))
#counterPos = dict(Counter(pos))
counterConcept = dict(Counter(concept))

#wordsRepetitions = dict(Counter(wordsRepetitions))

weights = []

for wc in counterWordConcept:
	wc, counter = wc
	w = wc.split("\t")[0]
	#p = wplc.split("\t")[1]
	#l = wplc.split("\t")[2]
	c = wc.split("\t")[1]	
	#count_pos = counterPos[p]
	count_word = counterWord[w]
	#count_lemma = counterLemma[l]
	count_concept = counterConcept[c]
	cost = -math.log(float(counter)/float(count_concept))
	
	weights.append({'word':w , 'concept':c, 'cost':cost})


with open('../data/wordToConcept.m', 'w') as f:
	for wlc in weights:
		#if wlc['word'] in wordsRepetitions and wordsRepetitions[wlc['word']] > 1 and wlc['concept'] in wordsRepetitions and wordsRepetitions[wlc['concept']] > 1 :
		f.write('0\t0\t' + wlc['word'] + '\t' + wlc['concept'] + '\t' + str(abs(wlc['cost'])) + '\n')
	for c in list(set(concept)):
		#print '0\t0\t' + "<unk>\t" + c + "\t0\n"
		#if c in wordsRepetitions and wordsRepetitions[c] > 1 :
		f.write('0\t0\t' + "<unk>\t" + c + "\t0\n")
		#f.write('0\t0\t' + "<unk>\t" + c + "\t" + str(abs(-math.log(float(counterConcept[c])/float(counterWords)))) + "\n")
	f.write('0')
