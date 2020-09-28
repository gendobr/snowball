import sys
import configparser
import jsonlines
import numpy
import lib.topicmodel as tm
import time
import fire
import os, json
import psutil


def stopwords(config=None, outfile=None, infile=None, dictfile=None, reduceddictfile=None):
    t0 = time.time()
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_name = '004_stopwords.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()


    # ===============================================================
    # file names
    if infile and os.path.isfile(infile):
        file_path_input = infile
    else:
        file_path_input = f'{data_dir}/003_joint_probabilities.npy'
    log(('input', file_path_input))

    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/004_stopwords_output.jsonl'
    log(('output', file_path_output))

    if dictfile and os.path.isfile(dictfile):
        file_path_dict = dictfile
    else:
        file_path_dict = f'{data_dir}/002_rarewords_reduceddict.jsonl'
    log(('dictfile', file_path_dict))

    if reduceddictfile:
        file_path_reduced_dict = reduceddictfile
    else:
        file_path_reduced_dict = f'{data_dir}/004_stopwords_reduceddict.jsonl'
    log(('reduceddictfile', file_path_reduced_dict))
    # /file names
    # ===============================================================
    topic_model = tm.Model(data_dir)

    with jsonlines.open(file_path_dict) as reader:
        topic_model.set_word_dictionary({row[0]: row[1] for row in reader})

    Hmax = conf.getfloat('main', 'Hmax')

    cooccurrence_probability = numpy.load(file_path_input)

    stopwords_dict = topic_model.stopwords(cooccurrence_probability, Hmax)
    log(("stopwords", stopwords_dict))
    with jsonlines.open(file_path_output, mode='w') as writer:
        for k in stopwords_dict:
            writer.write([k, stopwords_dict[k]])

    # exclude rare words from word_dictionary
    reduced_word_dictionary = topic_model.reduced_dictionary(topic_model.word_dictionary, stopwords_dict, {})
    with jsonlines.open(file_path_reduced_dict, mode='w') as writer:
        for k in reduced_word_dictionary:
            writer.write([k, reduced_word_dictionary[k]])
    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(stopwords)
