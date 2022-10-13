#!/bin/sh
ddr=../data/$1
pipenv run python \
   004_stopwords.py --config=$ddr/config.ini \
                    --infile=$ddr/003_joint_probabilities.npy \
                    --outfile=$ddr/004_stopwords_output.jsonl \
                    --dictfile=$ddr/002_rarewords_reduceddict.jsonl \
                    --reduceddictfile=$ddr/004_stopwords_reduceddict.jsonl