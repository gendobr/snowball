# import sys
import fire
import configparser
import time
# import lib.ate as ate
import json
import os
import psutil
import jsonlines
from nltk.stem.porter import *
from os import listdir
from os.path import isfile, join


def do_clear_terms(config=None,
                 in_dir_terms=None,  #
                 out_dir_terms=None,
                 stopwords=None,
                 trace=0
                 ):
    """

    :param config:
    :param in_terms: input TXT file
    :param out_terms: output CSV file containing terms
    :param stopwords: text file containing stopwords, one word per row
    :param trace: show detailed information about execution
    :return:
    """
    t0 = time.time()

    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_name = '017_ate_clear_terms.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    f_stopwords = open(stopwords, 'r')
    stopwords = [r.strip() for r in f_stopwords.readlines() if len(r.strip()) > 0]
    f_stopwords.close()

    if not os.path.isdir(out_dir_terms):
        log(f'pdf dir {out_dir_terms} not found. Creating')
        os.mkdir(out_dir_terms)

    in_term_files = sorted([f for f in listdir(in_dir_terms) if f.lower().endswith(".txt")])

    for in_term_file in in_term_files:
        t2 = time.time()
        in_terms = join(in_dir_terms, in_term_file)
        with jsonlines.open(in_terms) as reader:
            terms = [row for row in reader]

        clear_terms = [row for row in terms if row[0] not in stopwords]
        out_terms = join(out_dir_terms, in_term_file)
        with jsonlines.open(out_terms, mode='w') as writer:
            for cv in clear_terms:
                writer.write(cv)
        t3 = time.time()
        log(("file", in_terms, "n_terms", len(terms),"time", t3 - t2,))
    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(do_clear_terms)


