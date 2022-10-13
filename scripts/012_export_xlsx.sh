#!/bin/sh
ddr=../data/$1
pipenv run python \
   012_export_xlsx.py --config=$ddr/config.ini \
                   --outfile=$ddr/012_exported.xlsx \
                   --initems=$ddr/011_download_pdfs.jsonl
