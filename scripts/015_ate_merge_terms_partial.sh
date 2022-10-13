#!/bin/sh
ddr=../data/openalex-test
poetry run python \
     015_ate_merge_terms_partial.py \
         --config=$ddr/config.ini \
         --dir_in_terms=$ddr/terms_partial  \
         --dir_out_terms=$ddr/terms_merged \
         --trace=0

