#!/bin/sh
pipenv run python \
   016_ate_get_terms.py \
       --config=../data/GAN/config.ini \
       --in_dir_dataset=../data/GAN/datasets \
       --out_dir_terms=../data/GAN/terms  \
       --stopwords=../data/GAN/ate_stopwords.csv  \
       --trace=0
