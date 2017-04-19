import os
import sys
from collections import Counter

file1_path = sys.argv[1]
file2_path = sys.argv[2]
words = []
#wordsRepetitions = []

#read file
text = None
with open(file1_path) as f:
	text = f.read()

lines = text.split("\n")
for line in lines:
	if not line: continue
	word = line.split("\t")
	#wordsRepetitions.append(word[0])
	#wordsRepetitions.append(word[1])
	if not word[0] in words: words.append(word[0])
	if not word[1] in words: words.append(word[1])
	#if not word[2] in words: words.append(word[2])

text = None
with open(file2_path) as f:
	text = f.read()

lines = text.split("\n")
for line in lines:
	if not line: continue
	word = line.split("\t")
	#wordsRepetitions.append(word[1])
	if not word[1] in words: words.append(word[1])

#sort words
words = sorted(words)

#wordsRepetitions = dict(Counter(wordsRepetitions))

counter = 0

with open('../data/lexicon', 'w') as f:
	f.write("<eps>\t" + str(counter) + "\n")
	counter = counter+1
	for word in words:
		#if word in wordsRepetitions and wordsRepetitions[word] > 1 :
		f.write(word + "\t" + str(counter) + "\n")
		counter = counter+1
	f.write("<unk>\t" + str(counter))
