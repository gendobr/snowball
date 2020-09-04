#!/bin/sh
pipenv run python \
   004_stopwords.py --config=../data/GAN/config.ini \
                    --infile=../data/GAN/003_joint_probabilities.npy \
                    --outfile=../data/GAN/004_stopwords_output.jsonl \
                    --dictfile=../data/GAN/002_rarewords_reduceddict.jsonl \
                    --reduceddictfile=../data/GAN/004_stopwords_reduceddict.jsonl