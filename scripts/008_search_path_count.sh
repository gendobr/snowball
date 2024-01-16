#!/bin/sh
ddr=../data/graphdb
poetry run python \
   008_search_path_count.py --config=$ddr/config.ini \
                   --outfile=$ddr/008_search_path_count_output.jsonl \
                   --initems=$ddr/007_restricted_snowball_output.jsonl \
                   --inedgelist=$ddr/008_search_path_count_edge_list.edgelist
