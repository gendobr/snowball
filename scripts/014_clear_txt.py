# import sys
import os.path
import time
import fire
import configparser
import datetime
import pandas as pd
from os import listdir
from os.path import isfile, join
import os
import lib.cleartxt as cleartxt



def do_clear_txt(config=None, rawtxtdir=None, cleartxtdir=None):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    # =====================================================
    # place to store extracted texts
    if cleartxtdir:
        clear_txt_dir = cleartxtdir
    else:
        clear_txt_dir = f'{data_dir}/clear_txts'
    print(('clear_txt_dir', clear_txt_dir))
    # =====================================================

    # =====================================================
    # place to read raw texts
    if rawtxtdir:
        raw_txt_dir = rawtxtdir
    else:
        raw_txt_dir = f'{data_dir}/txts'
    print(('raw_txt_dir', raw_txt_dir))
    # =====================================================

    # =====================================================
    # read raw txt files
    raw_txt_files = sorted([(raw_txt_dir, f) for f in listdir(raw_txt_dir) if isfile(join(raw_txt_dir, f)) and f.lower().endswith(".txt")])
    print(raw_txt_files)
    for f in raw_txt_files:
        fpath_out = join(clear_txt_dir, f[1][:-4] + '.txt')
        print(raw_txt_dir, '/', f[1], "=>", fpath_out)
        ftxt = open(fpath_out, 'w')
        try:
            # ftxt.write(ate.pdf_to_text_textract(join(f[0], f[1])).replace("\n"," "))
            # file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
            file_content = cleartxt.clean_text(join(f[0], f[1]))
            ftxt.write(file_content)
        except TypeError as e:
            print("error writing file " + fpath_out)
            print(e)
            print("\n\n")
        ftxt.close()

    # =====================================================


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_clear_txt)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
