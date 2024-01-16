#!/bin/sh
ddr=../data/bim
poetry run python \
   013_ate_clear_txt.py --config=$ddr/config.ini \
                   --rawtxtdir=$ddr/txts \
                   --cleartxtdir=$ddr/clear_txts
