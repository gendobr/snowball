# import sys
import fire
import configparser
import time
import lib.ate as ate
import re
import csv
import os
import psutil
import json
import jsonlines


def do_get_terms(config=None,
                 in_dataset=None,  #
                 out_terms=None,
                 stopwords=None,
                 trace=0
                 ):
    """

    :param config:
    :param in_dataset: input TXT file
    :param out_terms: output CSV file containing terms
    :param stopwords: text file containing stopwords, one word per row
    :param term_patterns: text file containing term patterns, one word per row
    :param min_term_words: number of words in one term
    :param min_term_length: minimal number of characters in the term
    :param trace: show detailed information about execution
    :return:
    """

    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    min_term_words = int(conf.get('ate', 'min_term_words'))
    min_term_length = int(conf.get('ate', 'min_term_length'))
    term_patterns = json.loads(conf.get('ate', 'term_patterns'))
    trace = (int(trace) == 1)

    f_stopwords = open(stopwords, 'r')
    stopwords = [r.strip() for r in f_stopwords.readlines() if len(r.strip()) > 0]
    f_stopwords.close()

    fp = open(in_dataset, "r")
    doc_txt = fp.read()
    fp.close()
    # doc_txt = unicode(doc_txt, "utf-8", errors='replace').replace(u'\ufffd', '_')
    doc_txt = doc_txt.replace(u'\ufffd', '_')
    doc_txt = re.sub(r'et +al\.', 'et al', doc_txt)
    doc_txt = re.split(r'[\r\n]', doc_txt)

    # print('len(text)=' + str( len(doc_txt) ) )

    term_extractor = ate.TermExtractor(
        stopwords=stopwords, term_patterns=term_patterns,
        min_term_words=min_term_words, min_term_length=min_term_length
    )
    terms = term_extractor.extract_terms(doc_txt, trace=trace)
    print('len(terms)=' + str(len(terms)))
    if trace:
        # print terms[:10]
        print("Term extraction finished")

    c_values = term_extractor.c_values(terms, trace=trace)   # replace this line

    with jsonlines.open(out_terms, mode='w') as writer:
        for cv in c_values:
            writer.write(cv)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_get_terms)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    print('used RAM(bytes)=', process.memory_info().rss)  # in bytes

