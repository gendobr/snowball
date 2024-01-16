#!/bin/sh
dir=graphdb
poetry run python \
   003_joint_probabilities.py --config=../data/$dir/config.ini \
                    --infile=../data/$dir/001_tokenizer_output.jsonl \
                    --outfile=../data/$dir/003_joint_probabilities.npy \
                    --indictfile=../data/$dir/002_rarewords_reduceddict.jsonl
                    