#!/bin/sh
ddr=../data/$1
pipenv run python \
   001_tokenizer.py --config=$ddr/config.ini \
                    --infile=$ddr/000_download_output.jsonl \
                    --outfile=$ddr/001_tokenizer_output.jsonl\
                    --outdictfile=$ddr/001_tokenizer_dict.jsonl