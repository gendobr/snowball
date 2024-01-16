#!/bin/sh
ddr=../data/graphdb
poetry run python \
   010_download_pdfs.py --config=$ddr/config.ini \
                   --outfile=$ddr/010_download_pdfs.jsonl \
                   --initems=$ddr/009_extend_items_google_scholar.jsonl \
                   --pdfdir=$ddr/pdfs
