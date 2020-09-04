#!/bin/sh
pipenv run python \
   001_tokenizer.py --config=../data/GAN/config.ini \
                    --infile=../data/GAN/000_download_output.jsonl \
                    --outfile=../data/GAN/001_tokenizer_output.jsonl\
                    --outdictfile=../data/GAN/001_tokenizer_dict.jsonl