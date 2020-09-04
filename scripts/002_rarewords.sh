#!/bin/sh
pipenv run python \
   002_rarewords.py --config=../data/GAN/config.ini \
                    --infile=../data/GAN/001_tokenizer_output.jsonl \
                    --outfile=../data/GAN/002_rarewords_output.jsonl \
                    --dictfile=../data/GAN/001_tokenizer_dict.jsonl \
                    --reduceddictfile=../data/GAN/002_rarewords_reduceddict.jsonl