#!/bin/sh
pipenv run python \
   015_ate_generate_datasets.py --config=../data/GAN/config.ini \
                   --datasetdir=../data/GAN/datasets \
                   --cleartxtdir=../data/GAN/clear_txts  \
                   --increment_size=20  \
                   --metadatafile=../data/GAN/011_download_pdfs.jsonl  \
                   --strategy="spc-desc"
