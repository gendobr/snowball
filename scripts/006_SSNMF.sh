#!/bin/sh
pipenv run python \
   006_SSNMF.py --config=../data/GAN/config.ini \
                   --outfile=../data/GAN/006_ssnmf_output.npy \
                   --infile=../data/GAN/005_reduced_joint_probabilities.npy \
                   --outptmfile=../data/GAN/006_ptm_output.npy
