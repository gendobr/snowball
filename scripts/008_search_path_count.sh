#!/bin/sh
pipenv run python \
   008_search_path_count.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/008_search_path_count_output.jsonl \
                   --initems=../data/GAN/007_restricted_snowball_output.jsonl \
                   --inedgelist=../data/GAN/008_search_path_count_edge_list.edgelist
