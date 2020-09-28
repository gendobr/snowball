import sys
import configparser
import psutil
import numpy
import lib.snmf as snmf
import lib.topicmodel as tm
import time
import fire
import os, json


def do_ssnmf(config=None, outfile=None, infile=None, outptmfile=None):
    t0 = time.time()
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_name = '006_SSNMF.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # ===============================================================
    # file names
    if infile and os.path.isfile(infile):
        file_path_input = infile
    else:
        file_path_input = f'{data_dir}/005_reduced_joint_probabilities.npy'
    log(('input', file_path_input))

    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/006_ssnmf_output.npy'
    log(('output', file_path_output))

    if outptmfile:
        file_path_ptm_output = outptmfile
    else:
        file_path_ptm_output = f'{data_dir}/006_ptm_output.npy'
    log(('outptmfile', file_path_ptm_output))

    # /file names
    # ===============================================================

    # read configuration file
    p_max = conf.getint('main', 'Pmax')
    lam = conf.getfloat('main', 'lambda')

    j_prob_reduced = numpy.load(file_path_input)
    log(("len(j_prob_reduced)=", len(j_prob_reduced)))

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
    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(do_ssnmf)
