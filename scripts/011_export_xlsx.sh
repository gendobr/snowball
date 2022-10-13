#!/bin/sh
ddr=../data/openalex-test
poetry run python \
   011_export_xlsx.py --config=$ddr/config.ini \
                   --outfile=$ddr/011_exported.xlsx \
                   --initems=$ddr/010_download_pdfs.jsonl
