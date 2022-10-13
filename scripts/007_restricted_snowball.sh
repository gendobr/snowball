#!/bin/sh
ddr=../data/openalex-test
poetry run python \
   007_restricted_snowball.py --config=$ddr/config.ini \
                   --outfile=$ddr/007_restricted_snowball_output.jsonl \
                   --inptmfile=$ddr/006_ptm_output.npy \
                   --indictfile=$ddr/004_stopwords_reduceddict.jsonl \
                   --incooccurrencefile=$ddr/005_reduced_joint_probabilities.npy
