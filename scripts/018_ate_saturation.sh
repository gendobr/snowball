#!/bin/sh
ddr=../data/$1
pipenv run python \
   018_ate_saturation.py \
       --config=$ddr/config.ini \
       --in_dir=$ddr/terms_clear \
       --out_thd=$ddr/018_thd.csv
