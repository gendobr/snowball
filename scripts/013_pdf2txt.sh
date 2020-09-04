#!/bin/sh
pipenv run python \
   013_pdf2txt.py --config=../data/GAN/config.ini \
                   --txtdir=../data/GAN/txts \
                   --pdfdir=../data/GAN/pdfs
