#!/bin/sh
pipenv run python \
   003_joint_probabilities.py --config=../data/GAN/config.ini \
                    --infile=../data/GAN/001_tokenizer_output.jsonl \
                    --outfile=../data/GAN/003_joint_probabilities.npy \
                    --indictfile=../data/GAN/001_tokenizer_dict.csv