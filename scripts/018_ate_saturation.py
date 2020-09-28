# import sys
import lib.thd as thd
import os, json
import jsonlines
from nltk.stem.porter import *
import pandas as pd
import time
import fire
import configparser
from os import listdir
from os.path import isfile, join
import psutil



def do_ate_saturation(
        config=None,
        in_dir=None,  #
        out_thd=None
        ):
    """
    :param config:
    :param in_dir: input TXT file
    :param out_thd: output CSV file containing terms
    :return:
    """
    t0 = time.time()
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_name = '018_ate_saturation.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    term_files = sorted([join(in_dir, f) for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.lower().endswith(".txt")])
    log(('term_files', term_files,))
    report = []

    for i in range(0, len(term_files) - 1):
        log("------starting new iteration--------")
        with jsonlines.open(term_files[i]) as reader:
            terms_1 = [row for row in reader]
        df_T1 = pd.DataFrame(data=terms_1, columns=['term', 'cvalue']).set_index('term')

        with jsonlines.open(term_files[i+1]) as reader:
            terms_2 = [row for row in reader]
        df_T2 = pd.DataFrame(data=terms_2, columns=['term', 'cvalue']).set_index('term')

        val_eps, val_thd, val_thdr = thd.thd(df_T1, df_T2)

        r = dict(
                file1=term_files[i],
                file2=term_files[i + 1],
                eps=val_eps,
                thdr=val_thdr,
                thd=val_thd
            )
        report.append(r)
        log(r)

    with jsonlines.open(out_thd, mode='w') as writer:
        for r in report:
            writer.write(r)

    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(do_ate_saturation)
