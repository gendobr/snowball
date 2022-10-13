#!/bin/sh
ddr=../data/$1
pipenv run python \
   003_joint_probabilities.py --config=$ddr/config.ini \
                    --infile=$ddr/001_tokenizer_output.jsonl \
                    --outfile=$ddr/003_joint_probabilities.npy \
                    --indictfile=$ddr/001_tokenizer_dict.csv