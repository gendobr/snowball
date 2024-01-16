#!/bin/sh
dir=graphdb
poetry run python \
   002_rarewords.py --config=../data/$dir/config.ini \
                    --infile=../data/$dir/001_tokenizer_output.jsonl \
                    --outfile=../data/$dir/002_rarewords_output.jsonl \
                    --dictfile=../data/$dir/001_tokenizer_dict.jsonl \
                    --reduceddictfile=../data/$dir/002_rarewords_reduceddict.jsonl
