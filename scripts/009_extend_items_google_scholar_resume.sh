#!/bin/sh
ddr=../data/$1
pipenv run python \
   010_extend_items_google_scholar.py --config=$ddr/config.ini \
                   --outfile=$ddr/010_extend_items_google_scholar.jsonl \
                   --initems=resume \
                   --searchauthor=0
