#!/bin/sh
ddr=../data/$1
pipenv run python \
   013_ate_pdf2txt.py --config=$ddr/config.ini \
                   --txtdir=$ddr/txts \
                   --pdfdir=$ddr/pdfs
