#!/bin/sh
ddr=../data/$1
pipenv run python \
   015_ate_generate_datasets.py --config=$ddr/config.ini \
                   --datasetdir=$ddr/datasets \
                   --cleartxtdir=$ddr/clear_txts  \
                   --increment_size=20  \
                   --metadatafile=$ddr/012_exported_edited.xlsx  \
                   --strategy="citation-per-year-desc"
