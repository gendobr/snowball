#!/bin/sh
poetry run python \
   001_tokenizer.py --config=../data/openalex-test/config.ini \
                    --infile=../data/openalex-test/000_download_output.jsonl \
                    --outfile=../data/openalex-test/001_tokenizer_output.jsonl\
                    --outdictfile=../data/openalex-test/001_tokenizer_dict.jsonl
