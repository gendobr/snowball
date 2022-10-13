#!/bin/sh
ddr="../data/$1"
pipenv run python \
   000_download.py --config=$ddr/config.ini \
                   --outfile=$ddr/000_download_output.jsonl \
                   --infile=resume
