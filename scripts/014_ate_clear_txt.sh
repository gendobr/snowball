#!/bin/sh
pipenv run python \
   014_ate_clear_txt.py --config=../data/GAN/config.ini \
                   --rawtxtdir=../data/GAN/txts \
                   --cleartxtdir=../data/GAN/clear_txts
