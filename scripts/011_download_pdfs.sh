#!/bin/sh
ddr=../data/$1
pipenv run python \
   011_download_pdfs.py --config=$ddr/config.ini \
                   --outfile=$ddr/011_download_pdfs.jsonl \
                   --initems=$ddr/010_extend_items_google_scholar.jsonl \
                   --pdfdir=$ddr/pdfs

#pipenv run python \
#   011_download_pdfs.py --config=$ddr/config.ini \
#                   --outfile=$ddr/011_download_pdfs.jsonl \
#                   --initems=resume \
#                   --pdfdir=$ddr/pdfs