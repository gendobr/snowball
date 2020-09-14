#!/bin/sh
pipenv run python \
     016_ate_get_terms.py \
         --config=../data/GAN/config.ini \
         --in_dir_dataset=../data/GAN/datasets_partial \
         --out_dir_terms=../data/GAN/terms_partial  \
         --stopwords=../data/GAN/ate_stopwords.csv  \
         --trace=0
