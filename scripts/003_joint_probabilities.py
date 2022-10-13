import sys
import numpy
import time
import fire
import configparser
import lib.topicmodel as tm
import jsonlines
import os, json
import psutil


def joint_probabilities(config=None, outfile=None, infile=None, indictfile=None):
    t0 = time.time()
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_path = os.path.join(data_dir, conf.get('003_joint_probabilities', 'log_file_name'))

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
        file_path_input = f'{data_dir}/001_tokenizer_output.jsonl'
    log(('input', file_path_input))

    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/003_joint_probabilities.npy'
    log(('output', file_path_output))

    if indictfile and os.path.isfile(indictfile):
        file_path_dict = indictfile
    else:
        file_path_dict = f'{data_dir}/001_tokenizer_dict.jsonl'
    log(('dictfile', file_path_dict))

    # /file names
    # ===============================================================
    topic_model = tm.Model(data_dir)

    with jsonlines.open(file_path_dict) as reader:
        topic_model.set_word_dictionary({row[0]: row[1] for row in reader})

    cooccurrence_probability = topic_model.coccurences(file_path_input, lambda it: it['tokens'])
    numpy.save(file_path_output, cooccurrence_probability)
    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(joint_probabilities)