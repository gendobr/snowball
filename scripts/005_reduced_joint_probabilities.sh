#!/bin/sh
ddr=../data/graphdb
poetry run python \
   003_joint_probabilities.py --config=$ddr/config.ini \
                    --infile=$ddr/001_tokenizer_output.jsonl \
                    --outfile=$ddr/005_reduced_joint_probabilities.npy \
                    --indictfile=$ddr/004_stopwords_reduceddict.jsonl
