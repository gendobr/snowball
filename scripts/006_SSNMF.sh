#!/bin/sh
ddr=../data/graphdb
poetry run python \
   006_SSNMF.py --config=$ddr/config.ini \
                   --outfile=$ddr/006_ssnmf_output.npy \
                   --infile=$ddr/005_reduced_joint_probabilities.npy \
                   --outptmfile=$ddr/006_ptm_output.npy
