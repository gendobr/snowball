#!/bin/sh
  pipenv run python \
     016_ate_merge_terms_partial.py \
         --config=../data/GAN/config.ini \
         --dir_in_terms=../data/GAN/terms_partial  \
         --dir_out_terms=../data/GAN/terms_merged \
         --trace=0

