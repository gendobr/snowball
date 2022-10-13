#!/bin/sh
poetry run python \
   002_rarewords.py --config=../data/openalex-test/config.ini \
                    --infile=../data/openalex-test/001_tokenizer_output.jsonl \
                    --outfile=../data/openalex-test/002_rarewords_output.jsonl \
                    --dictfile=../data/openalex-test/001_tokenizer_dict.jsonl \
                    --reduceddictfile=../data/openalex-test/002_rarewords_reduceddict.jsonl
