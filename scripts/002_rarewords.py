import sys

import configparser
import time
import fire
import lib.topicmodel as tm
import os
import csv
import jsonlines


def rare_words(config=None, outfile=None, infile=None, dictfile=None, reduceddictfile=None):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    alpha = conf.getfloat('main', 'alpha')

    # ===============================================================
    # file names
    if infile and os.path.isfile(infile):
        file_path_input = infile
    else:
        file_path_input = f'{data_dir}/001_tokenizer_output.jsonl'
    print(('input', file_path_input))

    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/002_rarewords_output.jsonl'
    print(('output', file_path_output))

    if dictfile and os.path.isfile(dictfile):
        file_path_dict = dictfile
    else:
        file_path_dict = f'{data_dir}/001_tokenizer_dict.jsonl'
    print(('dictfile', file_path_dict))

    if reduceddictfile:
        file_path_reduced_dict = reduceddictfile
    else:
        file_path_reduced_dict = f'{data_dir}/002_rarewords_reduceddict.jsonl'
    print(('reduceddictfile', file_path_reduced_dict))
    # /file names
    # ===============================================================

    topic_model = tm.Model(data_dir)

    word_dictionary = dict()
    with jsonlines.open(file_path_dict) as reader:
        for row in reader:
            word_dictionary[row[0]] = row[1]

    topic_model.set_word_dictionary(word_dictionary)

    rare_words_dict = topic_model.rare_words_memory_optimal(
        file_path_input,
        alpha,
        lambda it: it['tokens']
    )

    with jsonlines.open(file_path_output, mode='w') as writer:
        for k in rare_words_dict:
            writer.write([k, rare_words_dict[k]])

    # exclude rare words from word_dictionary
    reduced_word_dictionary = topic_model.reduced_dictionary(word_dictionary, {}, rare_words_dict)
    with jsonlines.open(file_path_reduced_dict, mode='w') as writer:
        for k in reduced_word_dictionary:
            writer.write([k, reduced_word_dictionary[k]])

    print("Dictionary size", len(word_dictionary), " => ", len(reduced_word_dictionary))


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(rare_words)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))