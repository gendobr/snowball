#!/bin/sh
pipenv run python \
   009_extend_items.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/009_extend_items_output.jsonl \
                   --initems=../data/GAN/008_search_path_count_output.jsonl

