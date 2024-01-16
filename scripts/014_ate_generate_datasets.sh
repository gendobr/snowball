#!/bin/sh
ddr=../data/bim
poetry run python \
   014_ate_generate_datasets.py --config=$ddr/config.ini \
                   --datasetdir=$ddr/datasets \
                   --cleartxtdir=$ddr/clear_txts  \
                   --increment_size=20  \
                   --metadatafile=$ddr/011_exported.xlsx  \
                   --strategy="spc-desc"
