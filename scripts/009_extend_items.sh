#!/bin/sh
ddr=../data/$1
pipenv run python \
   009_extend_items.py --config=$ddr/config.ini \
                   --outfile=$ddr/009_extend_items_output.jsonl \
                   --initems=$ddr/008_search_path_count_output.jsonl

