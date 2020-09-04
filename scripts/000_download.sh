#!/bin/sh
pipenv run python \
   000_download.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/000_download_output.jsonl \
                   --infile=resume
