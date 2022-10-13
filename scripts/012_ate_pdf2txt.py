import time
import fire
import configparser
from os import listdir
from os.path import isfile, join
import psutil
import os
import lib.pdf2txt as pdf2txt
import json


def do_pdf2txt(config=None, txtdir=None, pdfdir=None):

    t0 = time.time()

    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    log_file_name = '012_ate_pdf2txt.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # =====================================================
    # place to store extracted texts
    if txtdir:
        txt_dir = txtdir
    else:
        txt_dir = f'{data_dir}/txts'

    if not os.path.isdir(txt_dir):
        log(f'pdf dir {txt_dir} not found. Creating')
        os.mkdir(txt_dir)

    log(('txt_dir', txt_dir))
    # =====================================================

    # =====================================================
    # place to read pdfs
    if pdfdir:
        pdf_dir = pdfdir
    else:
        pdf_dir = f'{data_dir}/pdfs'

    if not os.path.isdir(pdf_dir):
        log(f'pdf dir {pdf_dir} not found. Exiting')
        os.mkdir(pdf_dir)

    log(('pdf_dir', pdf_dir))
    # =====================================================

    # =====================================================
    # read pdf files
    pdf_files = sorted([(pdfdir, f) for f in listdir(pdfdir) if isfile(join(pdfdir, f)) and f.lower().endswith(".pdf")])
    log(pdf_files)
    for f in pdf_files:
        fpath_out = join(txtdir, f[1][:-4] + '.txt')
        log((pdfdir, '/', f[1], "=>", fpath_out))
        ftxt = open(fpath_out, 'wb')
        try:
            # ftxt.write(ate.pdf_to_text_textract(join(f[0], f[1])).replace("\n"," "))
            # file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
            # file_content = pdf2txt.pdf_to_text_textract(join(f[0], f[1]))
            file_content = ''
            # try:
            #     file_content = pdf2txt.pdf_to_text_pycpdf(join(f[0], f[1]))
            #     log('pdf_to_text_pycpdf')
            # except:
            #     file_content = ''

            if len(file_content) == 0:
                try:
                    file_content = pdf2txt.pdf_to_text_pymupdf(join(f[0], f[1]))
                    log('pdf_to_text_pymupdf')
                except:
                    file_content = ''
                
            if len(file_content) == 0:
                try:
                    file_content = pdf2txt.pdf_to_text_textract(join(f[0], f[1]))
                    log('pdf_to_text_textract')
                except:
                    file_content = ''

            ftxt.write(file_content)
        except TypeError as e:
            log(("error writing file ", fpath_out))
            log((str(e),))
            log(("\n\n", ))

        # file_content=ate.pdf_to_text_textract(join(f[0], f[1]))
        # file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
        # ftxt.write(file_content)

        ftxt.close()

    t1 = time.time()
    log(("finished",))
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes
    # =====================================================


if __name__ == "__main__":
    fire.Fire(do_pdf2txt)

