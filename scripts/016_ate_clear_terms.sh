#!/bin/sh
ddr=../data/openalex-test
poetry run python  \
   016_ate_clear_terms.py \
       --config=$ddr/config.ini \
       --in_dir_terms=$ddr/terms \
       --out_dir_terms=$ddr/terms_clear \
       --stopwords=$ddr/ate_stopwords.csv  \
       --trace=0
