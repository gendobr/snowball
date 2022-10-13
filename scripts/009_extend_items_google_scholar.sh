#!/bin/sh
ddr=../data/openalex-test

# poetry run python \
#    009_extend_items_google_scholar.py --config=$ddr/config.ini \
#                    --outfile=$ddr/009_extend_items_google_scholar.jsonl \
#                    --initems=$ddr/008_search_path_count_output.jsonl

poetry run python \
  009_extend_items_google_scholar.py --config=$ddr/config.ini \
                  --outfile=$ddr/009_extend_items_google_scholar.jsonl \
                  --initems=resume

# poetry run python \
#   009_extend_items_google_scholar.py --config=$ddr/config.ini \
#                   --outfile=$ddr/009_extend_items_google_scholar.jsonl \
#                   --initems=resume \
#                   --searchauthor=0
