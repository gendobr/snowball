#!/bin/sh
pipenv run python \
   017_ate_clear_terms.py \
       --config=../data/GAN/config.ini \
       --in_dir_terms=../data/GAN/terms \
       --out_dir_terms=../data/GAN/terms_clear \
       --stopwords=../data/GAN/ate_stopwords.csv  \
       --trace=0
