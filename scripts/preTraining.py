import os
import sys

train_data = sys.argv[1]
new = []

#read file
text = None
with open(train_data) as f:
	text = f.read()

lines = text.split("\n")
for line in lines:
	if not line: new.append("\n")
	else :
		word = line.split("\t")
		if word[1] == "O" : new.append(line + "-" + word[0])
		else : new.append(line)

with open('../data/trainData', 'w') as f:
	for line in new:
		if line == "\n" : f.write(line)
		else : f.write(line+"\n")
