import sys
import numpy
import time
import fire
import configparser
import lib.topicmodel as tm
import jsonlines
import os


def joint_probabilities(config=None, outfile=None, infile=None, indictfile=None):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
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
        file_path_output = f'{data_dir}/003_joint_probabilities.npy'
    print(('output', file_path_output))

    if indictfile and os.path.isfile(indictfile):
        file_path_dict = indictfile
    else:
        file_path_dict = f'{data_dir}/001_tokenizer_dict.jsonl'
    print(('dictfile', file_path_dict))

    # /file names
    # ===============================================================
    topic_model = tm.Model(data_dir)

    with jsonlines.open(file_path_dict) as reader:
        topic_model.set_word_dictionary({row[0]: row[1] for row in reader})

    cooccurrence_probability = topic_model.coccurences(file_path_input, lambda it: it['tokens'])
    numpy.save(file_path_output, cooccurrence_probability)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(joint_probabilities)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))