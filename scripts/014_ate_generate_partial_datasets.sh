#!/bin/sh
ddr=../data/openalex-test
poetry run python \
   014_ate_generate_datasets.py --config=$ddr/config.ini \
                   --datasetdir=$ddr/datasets_partial \
                   --cleartxtdir=$ddr/clear_txts  \
                   --increment_size=20  \
                   --metadatafile=$ddr/011_download_pdfs.jsonl  \
                   --strategy="partial-spc-desc"
