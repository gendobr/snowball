#!/bin/sh
ddr=../data/openalex-test
poetry run python \
     015_ate_get_terms.py \
         --config=$ddr/config.ini \
         --in_dir_dataset=$ddr/datasets_partial \
         --out_dir_terms=$ddr/terms_partial  \
         --stopwords=$ddr/ate_stopwords.csv  \
         --trace=0
