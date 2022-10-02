#!/bin/sh
ddr=../data/$1
pipenv run python \
   016_ate_get_terms.py \
       --config=$ddr/config.ini \
       --in_dir_dataset=$ddr/datasets \
       --out_dir_terms=$ddr/terms  \
       --stopwords=$ddr/ate_stopwords.csv  \
       --trace=0
