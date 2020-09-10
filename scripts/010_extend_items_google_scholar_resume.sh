#!/bin/sh
pipenv run python \
   010_extend_items_google_scholar.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/010_extend_items_google_scholar.jsonl \
                   --initems=resume \
                   --searchauthor=0
