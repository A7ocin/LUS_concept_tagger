import sys
import math

train_tags = sys.argv[1]
test_sentences = sys.argv[2]

# read feats train file
with open(train_tags) as f:
	text = f.read()

# read data test file
with open(test_sentences) as f:
	text2 = f.read()

lines = text.split('\n')
lines2 = text2.split('\n')

with open('../data/trainTags', 'w') as f:
	for line in lines:
		if not line: 
			f.write('\n')
		else:
			concept = line.split('\t')[1]
			f.write(str(concept)+" ")

lines = []

with open('../data/trainTags', 'r') as f:
	for line in f:
		if line != "\n" : lines.append(line.rstrip())

with open('../data/testSentences', 'w') as f2:
	for line in lines2:
		if not line: 
			f2.write('\n')
		else:
			word = line.split('\t')[0]
			f2.write(str(word)+" ")

lines2 = []

with open('../data/testSentences', 'r') as f2:
	for line in f2:
		if line != "\n" : lines2.append(line.rstrip())
		
with open('../data/trainTags', 'w') as f:
	for line in lines:
		if not line: f.write("\n")
		f.write(line)
		f.write("\n")

with open('../data/testSentences', 'w') as f2:
	for line in lines2:
		if not line: f2.write("\n")
		f2.write(line)
		f2.write("\n")
		
