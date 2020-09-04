import sys
import configparser
import jsonlines
import numpy
import lib.snmf as snmf
import lib.topicmodel as tm
import time
import fire
import os


def do_ssnmf(config=None, outfile=None, infile=None, outptmfile=None):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    # ===============================================================
    # file names
    if infile and os.path.isfile(infile):
        file_path_input = infile
    else:
        file_path_input = f'{data_dir}/005_reduced_joint_probabilities.npy'
    print(('input', file_path_input))

    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/006_ssnmf_output.npy'
    print(('output', file_path_output))

    if outptmfile:
        file_path_ptm_output = outptmfile
    else:
        file_path_ptm_output = f'{data_dir}/006_ptm_output.npy'
    print(('outptmfile', file_path_ptm_output))

    # /file names
    # ===============================================================

    # read configuration file
    p_max = conf.getint('main', 'Pmax')
    lam = conf.getfloat('main', 'lambda')

    j_prob_reduced = numpy.load(file_path_input)
    print("len(j_prob_reduced)=", len(j_prob_reduced))

    topic_model = tm.Model(data_dir)

    params = {
        'maxIterations': 50,
        'lambda': lam,
        'eta': 0.1,
        'beta': 0.99,
        'beta2': 1.000,
        'maxError': 1e-7,
    }

    for i in range(0, 20):

        h = snmf.gradient_descent(j_prob_reduced, p_max, params)
        params['H'] = h

        # h = snmf.sparse_gradient_descent(j_prob_reduced, p_max, params)
        # params['H'] = h

        # h = snmf.sparse_multiplicative(j_prob_reduced, p_max, params)
        # params['H'] = h

        # h = snmf.gradient_descent(j_prob_reduced, p_max, params)
        # params['H'] = h

        numpy.save(file_path_output, h)

        TM = topic_model.model_from_factor(h)
        numpy.save(file_path_ptm_output, TM)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_ssnmf)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
