#!/bin/sh
for n in "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12"
do
  echo $n
  pipenv run python \
     017_ate_clear_terms.py \
         --config=../data/GAN/config.ini \
         --in_terms=../data/GAN/terms/T00000000$n.txt \
         --out_terms=../data/GAN/terms_clear/T00000000$n.txt  \
         --stopwords=../data/GAN/ate_stopwords.csv  \
         --trace=0
done
