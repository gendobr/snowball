#!/bin/sh
pipenv run python \
   007_restricted_snowball.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/007_restricted_snowball_output.jsonl \
                   --inptmfile=../data/GAN/006_ptm_output.npy \
                   --indictfile=../data/GAN/004_stopwords_reduceddict.jsonl \
                   --incooccurrencefile=../data/GAN/005_reduced_joint_probabilities.npy
