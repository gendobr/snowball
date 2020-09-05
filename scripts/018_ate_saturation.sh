#!/bin/sh
pipenv run python \
   018_ate_saturation.py \
       --config=../data/GAN/config.ini \
       --in_dir=../data/GAN/terms_clear \
       --out_thd=../data/GAN/018_thd.txt
