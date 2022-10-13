#!/bin/sh
ddr=../data/openalex-test
poetry run python \
   015_ate_get_terms.py \
       --config=$ddr/config.ini \
       --in_dir_dataset=$ddr/datasets \
       --out_dir_terms=$ddr/terms  \
       --stopwords=$ddr/ate_stopwords.csv  \
       --trace=0
