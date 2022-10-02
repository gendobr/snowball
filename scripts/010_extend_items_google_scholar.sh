#!/bin/sh
ddr=../data/$1

pipenv run python \
   010_extend_items_google_scholar.py --config=$ddr/config.ini \
                   --outfile=$ddr/010_extend_items_google_scholar.jsonl \
                   --initems=$ddr/009_extend_items_output.jsonl

#pipenv run python \
#   010_extend_items_google_scholar.py --config=$ddr/config.ini \
#                   --outfile=$ddr/010_extend_items_google_scholar.jsonl \
#                   --initems=resume

#pipenv run python \
#   010_extend_items_google_scholar.py --config=$ddr/config.ini \
#                   --outfile=$ddr/010_extend_items_google_scholar.jsonl \
#                   --initems=resume \
#                   --searchauthor=0
