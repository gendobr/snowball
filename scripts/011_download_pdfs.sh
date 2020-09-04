#!/bin/sh
pipenv run python \
   011_download_pdfs.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/011_download_pdfs.jsonl \
                   --initems=../data/GAN/010_extend_items_google_scholar.jsonl \
                   --pdfdir=../data/GAN/pdfs

#pipenv run python \
#   011_download_pdfs.py --config=../data/GAN/config.ini \
#                   --outfile=../data/GAN/011_download_pdfs.jsonl \
#                   --initems=resume \
#                   --pdfdir=../data/GAN/pdfs