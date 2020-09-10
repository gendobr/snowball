# import sys
import fire
import configparser
import time
import lib.ate as ate
import re
import os
import psutil
import jsonlines
from nltk.stem.porter import *
# from nltk.corpus import stopwords


def do_clear_terms(config=None,
                 in_terms=None,  #
                 out_terms=None,
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

    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    # data_dir = conf.get('main', 'data_dir')
    trace = (int(trace) == 1)

    with jsonlines.open(in_terms) as reader:
        terms = [row for row in reader]

    f_stopwords = open(stopwords, 'r')
    stopwords = [r.strip() for r in f_stopwords.readlines() if len(r.strip()) > 0]
    f_stopwords.close()
    # stemmer = PorterStemmer()
    # def has_stopwords(wrd):
    #     ws = str(wrd).split(' ')
    #     for w in ws:
    #         w_stemmed = stemmer.stem(w).encode('utf-8')
    #         if w_stemmed in stopwords:
    #             return True
    #     return False
    # clear_terms = [row for row in terms if not has_stopwords(row[0])]

    clear_terms = [row for row in terms if row[0] not in stopwords]

    with jsonlines.open(out_terms, mode='w') as writer:
        for cv in clear_terms:
            writer.write(cv)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_clear_terms)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    print('used RAM(bytes)=', process.memory_info().rss)  # in bytes

