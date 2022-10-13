#!/bin/sh
poetry run python \
   003_joint_probabilities.py --config=../data/openalex-test/config.ini \
                    --infile=../data/openalex-test/001_tokenizer_output.jsonl \
                    --outfile=../data/openalex-test/003_joint_probabilities.npy \
                    --indictfile=../data/openalex-test/001_tokenizer_dict.csv
                    