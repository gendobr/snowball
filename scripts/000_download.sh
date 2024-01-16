#!/bin/sh
poetry run python \
   000_download.py --config=../data/graphdb/config.ini \
                   --outfile=../data/graphdb/000_download_output.jsonl \
                   --infile=../data/graphdb/in-seed.csv
