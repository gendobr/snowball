#!/bin/sh
# pipenv run python \
#    010_extend_items_google_scholar.py --config=../data/GAN/config.ini \
#                    --outfile=../data/GAN/010_extend_items_google_scholar.jsonl \
#                    --initems=../data/GAN/009_extend_items_output.jsonl \
#                    --searchauthor=0
#  pipenv run python \
#    010_extend_items_google_scholar.py --config=../data/GAN/config.ini \
#                    --outfile=../data/GAN/010_extend_items_google_scholar.jsonl \
#                    --initems=resume \
#                    --searchauthor=0

pipenv run python \
   010_extend_items_google_scholar.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/010_extend_items_google_scholar.jsonl \
                   --initems=resume \
                   --searchauthor=0
