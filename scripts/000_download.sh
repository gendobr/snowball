#!/bin/sh
poetry run python \
   000_download.py --config=../data/openalex-test/config.ini \
                   --outfile=../data/openalex-test/000_download_output.jsonl \
                   --infile=resume
