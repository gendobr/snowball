# import sys
import lib.thd as thd
import os
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

    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    # data_dir = conf.get('main', 'data_dir')
    # trace = (int(trace) == 1)

    term_files = sorted([join(in_dir, f) for f in listdir(in_dir) if isfile(join(in_dir, f)) and f.lower().endswith(".txt")])
    print(('term_files', term_files,))
    report = []

    for i in range(0, len(term_files) - 1):
        print("------starting new iteration--------")
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
        print(r)

    with jsonlines.open(out_thd, mode='w') as writer:
        for r in report:
            writer.write(r)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_ate_saturation)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    print('used RAM(bytes)=', process.memory_info().rss)  # in bytes

