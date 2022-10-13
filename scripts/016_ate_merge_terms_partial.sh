#!/bin/sh
ddr=../data/$1
pipenv run python \
     016_ate_merge_terms_partial.py \
         --config=$ddr/config.ini \
         --dir_in_terms=$ddr/terms_partial  \
         --dir_out_terms=$ddr/terms_merged \
         --trace=0

