#!/bin/sh
ddr=../data/$1
pipenv run python \
   014_ate_clear_txt.py --config=$ddr/config.ini \
                   --rawtxtdir=$ddr/txts \
                   --cleartxtdir=$ddr/clear_txts
