#!/bin/sh
ddr=../data/$1
pipenv run python \
   002_rarewords.py --config=$ddr/config.ini \
                    --infile=$ddr/001_tokenizer_output.jsonl \
                    --outfile=$ddr/002_rarewords_output.jsonl \
                    --dictfile=$ddr/001_tokenizer_dict.jsonl \
                    --reduceddictfile=$ddr/002_rarewords_reduceddict.jsonl