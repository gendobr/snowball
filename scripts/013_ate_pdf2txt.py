import time
import fire
import configparser
from os import listdir
from os.path import isfile, join
import psutil
import lib.pdf2txt as pdf2txt


def do_pdf2txt(config=None, txtdir=None, pdfdir=None):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    # =====================================================
    # place to store extracted texts
    if txtdir:
        txt_dir = txtdir
    else:
        txt_dir = f'{data_dir}/txts'
    print(('txt_dir', txt_dir))
    # =====================================================

    # =====================================================
    # place to read pdfs
    if pdfdir:
        pdf_dir = pdfdir
    else:
        pdf_dir = f'{data_dir}/pdfs'
    print(('pdf_dir', pdf_dir))
    # =====================================================

    # =====================================================
    # read pdf files
    pdf_files = sorted([(pdfdir, f) for f in listdir(pdfdir) if isfile(join(pdfdir, f)) and f.lower().endswith(".pdf")])
    print(pdf_files)
    for f in pdf_files:
        fpath_out = join(txtdir, f[1][:-4] + '.txt')
        print(pdfdir, '/', f[1], "=>", fpath_out)
        ftxt = open(fpath_out, 'wb')
        try:
            # ftxt.write(ate.pdf_to_text_textract(join(f[0], f[1])).replace("\n"," "))
            # file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
            file_content = pdf2txt.pdf_to_text_textract(join(f[0], f[1]))
            ftxt.write(file_content)
        except TypeError as e:
            print("error writing file " + fpath_out)
            print(e)
            print("\n\n")

        # file_content=ate.pdf_to_text_textract(join(f[0], f[1]))
        # file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
        # ftxt.write(file_content)

        ftxt.close()

    # =====================================================


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_pdf2txt)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    print('used RAM(bytes)=', process.memory_info().rss)  # in bytes
