#!/bin/sh
pipenv run python \
   012_export_xlsx.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/012_exported.xlsx \
                   --initems=../data/GAN/011_download_pdfs.jsonl
