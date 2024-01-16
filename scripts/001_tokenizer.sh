#!/bin/sh
dir=graphdb
poetry run python \
   001_tokenizer.py --config=../data/$dir/config.ini \
                    --infile=../data/$dir/000_download_output.jsonl \
                    --outfile=../data/$dir/001_tokenizer_output.jsonl\
                    --outdictfile=../data/$dir/001_tokenizer_dict.jsonl
