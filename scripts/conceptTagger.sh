#!/bin/bash

clear

#Remove previous existing files and folders
if [ -d "../fst" ]; then 
	rm -r ../fst 
fi

if [ -d "../sentencesFst" ]; then 
	rm -r ../sentencesFst 
fi

if [ -d "../results" ]; then 
	rm -r ../results 
fi

if [ -f "../data/composition" ]; then 
	rm ../data/all.file.text.txt 
fi

if [ -f "../data/lexicon" ]; then 
	rm ../data/lexicon 
fi

if [ -f "../data/testSentences" ]; then 
	rm ../data/testSentences 
fi

if [ -f "../data/trainTags" ]; then 
	rm ../data/trainTags 
fi

if [ -f "../data/trainTags.m" ]; then 
	rm ../data/wordToLemma.m 
fi

if [ -f "../data/wordToConcept.m" ]; then 
	rm ../data/wordToConcept.m 
fi

if [ -f "../data/lemmaToConcept.m" ]; then 
	rm ../data/lemmaToConcept.m 
fi

#Create fst and results folders
mkdir ../fst
mkdir ../results
mkdir ../sentencesFst
mkdir ../results/outputData

#Extract sets
	python extractSets.py ../data/NLSPARQL.train.data ../data/NLSPARQL.test.data

#Create lexicon
python createLexicon.py ../data/NLSPARQL.train.feats.txt ../data/NLSPARQL.train.data

#Transducer word to concept
python wordToConcept.py ../data/NLSPARQL.train.feats.txt ../data/NLSPARQL.train.data

fstcompile --isymbols=../data/lexicon --osymbols=../data/lexicon ../data/wordToConcept.m > ../fst/wordToConcept.fst

echo "Method $1, $2-gram"
farcompilestrings --symbols=../data/lexicon --unknown_symbol='<unk>' ../data/trainTags > ../fst/trainTags.far
ngramcount --order=$2 --require_symbols=false ../fst/trainTags.far > ../fst/pos.cnt
ngrammake --method=$1 ../fst/pos.cnt > ../fst/languageModel.lm
farcompilestrings --symbols=../data/lexicon --unknown_symbol='<unk>' ../data/testSentences > ../fst/testSentences.far

cd ../sentencesFst; farextract --filename_suffix=.fst ../fst/testSentences.far; cd ../scripts;

echo "Composing the transducers. Please wait..."
for f in ../sentencesFst/*
do
    fstcompose $f ../fst/wordToConcept.fst |\
	fstcompose - ../fst/languageModel.lm |\
	fstrmepsilon |\
	fstshortestpath |\
	fsttopsort |\
	fstprint --isymbols=../data/lexicon --osymbols=../data/lexicon  >> ../results/composition;
done

#echo "Composition complete"
#wc -l ../results/composition

awk '{print $4}' ../results/composition > ../results/results

#echo "Complete"
#wc -l ../results/results

paste -d '\t' ../data/NLSPARQL.test.data ../results/results > ../results/to_evaluate_tabs

sed 's/\t/ /g' ../results/to_evaluate_tabs > ../results/to_evaluate

output="$1 $2"
perl ../scripts/conlleval.pl -d "\t" < ../results/to_evaluate_tabs > ../results/outputData/"${output}"
rm ../results/composition
echo "Done."
echo ""

echo "Tagging complete. See results @ /results/outputData"



