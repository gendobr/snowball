#!/usr/bin/env python2
# encoding: UTF-8

# import sys
import os.path
import os
from lib.openalex import Api
import time
import fire
import configparser
import json
import jsonlines
import csv
import queue
import lib.topicmodel as tm
import lib.nlp as nlp
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import numpy
import lib.measures as measures
import psutil


def snowball(config=None,
             outfile=None,
             infile=None,
             inptmfile=None,
             incooccurrencefile=None,
             indictfile=None):
    t0 = time.time()

    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_path = os.path.join(data_dir, conf.get('007_restricted_snowball', 'log_file_name'))

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # =========

    include_topics = json.loads(conf.get('openalex', 'openalexIncludeTopicsIds'))
    exclude_topics = json.loads(conf.get('openalex', 'openalexExcludeTopicsIds'))
    max_distance = conf.getfloat('007_restricted_snowball', 'maxDistance')
    measure = conf.get('007_restricted_snowball', 'measure')
    measure_types = {
        'kl': measures.kl_divergence,
        'skl': measures.skl_divergence,
        'js': measures.js_divergence,
        'hell': measures.hellinger_distance
    }
    if measure in measure_types:
        difference = measure_types[measure]
    else:
        log(('undefines measure ', measure, 'available types are ', measure_types))
        exit()

    api = Api(include_topics)

    # =====================================================
    # load initial ids to queue
    file_path_queued_ids = os.path.join(data_dir, conf.get('007_restricted_snowball', 'file_path_queued_ids')) # queued items
    file_path_seed_ids = os.path.join(data_dir, conf.get('007_restricted_snowball', 'file_path_seed_ids'))  # seed item ids

    log(('infile', infile))
    if infile and infile == 'resume' and os.path.isfile(file_path_queued_ids):
        file_path_initial_queued_ids = file_path_queued_ids
    elif infile and os.path.isfile(infile):
        if os.path.isfile(file_path_queued_ids):
            os.remove(file_path_queued_ids)
        file_path_initial_queued_ids = infile
    else:
        if os.path.isfile(file_path_queued_ids):
            os.remove(file_path_queued_ids)
        file_path_initial_queued_ids = file_path_seed_ids
    log(('file_path_initial_queued_ids', file_path_initial_queued_ids))

    queued_ids_set = set()
    queued_ids = queue.Queue()
    with open(file_path_initial_queued_ids, newline='') as csvfile:
        queue_reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
        for row in queue_reader:
            item_id = str(row[0])
            if item_id not in queued_ids_set:
                queued_ids_set.add(item_id)
                queued_ids.put(item_id)
    # =====================================================

    # =====================================================
    # load known ids
    file_path_known_ids = os.path.join(data_dir, conf.get('007_restricted_snowball', 'file_path_known_ids'))   # items that were downloaded
    known_ids = set()
    if infile and infile == 'resume' and os.path.isfile(file_path_known_ids):
        with open(file_path_known_ids, newline='') as csvfile:
            queue_reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            for row in queue_reader:
                known_ids.add(str(row[0]))
    elif  os.path.isfile(file_path_known_ids):
        os.remove(file_path_known_ids)
    # /load known ids
    # =====================================================

    # =====================================================
    # load done ids
    file_path_done_ids = os.path.join(data_dir, conf.get('007_restricted_snowball', 'file_path_done_ids'))   # items that were in the queue
    done_ids = set()
    if infile and infile == 'resume' and os.path.isfile(file_path_done_ids):
        with open(file_path_done_ids, newline='') as csvfile:
            queue_reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            for row in queue_reader:
                item_id = str(row[0])
                # queued_ids_set.add(item_id) ????
                done_ids.add(item_id)
    elif  os.path.isfile(file_path_done_ids):
        os.remove(file_path_done_ids)
    # /load done ids
    # =====================================================

    # =====================================================
    # dictionary
    if indictfile and os.path.isfile(indictfile):
        file_path_dict = indictfile
    else:
        file_path_dict = f'{data_dir}/001_tokenizer_dict.jsonl'
    log(('indictfile', file_path_dict))
    with jsonlines.open(file_path_dict) as reader:
        word_dictionary = {row[0]: row[1] for row in reader}
    # /dictionary
    # =====================================================

    # =====================================================
    # cooccurrence
    if incooccurrencefile and os.path.isfile(incooccurrencefile):
        file_path_cooccurrence = incooccurrencefile
    else:
        file_path_cooccurrence = f'{data_dir}/005_reduced_joint_probabilities.npy'
    log(('incooccurrencefile', file_path_cooccurrence))
    j_prob_reduced = numpy.load(file_path_cooccurrence)
    # /cooccurrence
    # =====================================================

    # =====================================================
    # PTM
    if inptmfile and os.path.isfile(inptmfile):
        file_path_ptm = inptmfile
    else:
        file_path_ptm = f'{data_dir}/006_ptm_output.npy'
    log(('inptmfile', file_path_ptm))
    ptm_data = numpy.load(file_path_ptm, allow_pickle=True)
    ptm_data = ptm_data.item()
    ptm = tm.Model(data_dir)
    ptm.set_word_dictionary(word_dictionary)
    ptm.load_topic_model(j_prob_reduced, ptm_data)
    # /PTM
    # =====================================================

    # =====================================================
    # place to store downloaded and selected item
    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/007_restricted_snowball_output.jsonl'

    if not ( infile and infile == 'resume' ) and  os.path.isfile(file_path_output):
        os.remove(file_path_output)

    log(('output', file_path_output))
    # =====================================================

    # =====================================================
    # load seeds
    log(('seed_ids_file', file_path_seed_ids))
    seed_ids = set()
    if not os.path.isfile(file_path_seed_ids):
        log(('error', 'message', 'seed not found', 'file_path_seed_ids', file_path_seed_ids))
        exit()
    with open(file_path_seed_ids, newline='') as csvfile:
        queue_reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
        for row in queue_reader:
            seed_ids.add(str(row[0]))
    log(('seed_ids', [x for x in seed_ids]))

    n_accepted_ids = 0
    seed_items = dict()
    if os.path.isfile(file_path_output):
        with jsonlines.open(file_path_output) as reader:
            for item in reader:
                n_accepted_ids += 1
                iten_id = str(item['id'])
                if iten_id in seed_ids:
                    seed_items[iten_id] = item
    log(('seed_items', [x for x in seed_items]))
    # =====================================================

    # =====================================================
    # init NLP tools
    ct = nlp.CustomTokenizer()
    ct.stemmer = PorterStemmer()
    ct.valid_pos_tags = {'NNP': 1, 'JJ': 1, 'NN': 1, 'NNS': 1, 'JJS': 1, 'JJR': 1, 'NNPS': 1}
    ct.tester = re.compile('^[a-zA-Z]+$')
    ct.stop = set(stopwords.words('english'))
    ct.word_dictionary = word_dictionary
    # /init NLP tools
    # =====================================================

    # =====================================================
    # snowball loop
    batch_size = int(conf.get('main', 'batch_size'))
    save_period = int(conf.get('main', 'save_period'))
    cnt = 0
    api_call_counter = 0
    while True:
        json_batch = []
        next_batch_ids = []
        if len(seed_items) == 0:
            next_batch_ids.extend([x for x in seed_ids])
            for item_id in next_batch_ids[batch_size:]:
                queued_ids_set.add(item_id)
                queued_ids.put(item_id)
            next_batch_ids = next_batch_ids[:batch_size]
            log(('seed_ids=>next_batch_ids', next_batch_ids))
        else:
            try:
                while len(next_batch_ids) < batch_size:
                    next_id = queued_ids.get_nowait()
                    if next_id not in done_ids:
                        next_batch_ids.append(next_id)
            except:
                pass
            log(('next_batch_ids', next_batch_ids))

        if len(next_batch_ids) == 0:
            break

        done_ids.update(next_batch_ids)

        items = api.load_by_ids(next_batch_ids, verbose=True)
        items.extend(api.load_by_rids(next_batch_ids, verbose=True))
        api_call_counter += 2
        log(('api_call_counter', api_call_counter, 'queue_size', queued_ids.qsize(), 'items', len(items)))
        n_known_items = 0
        for item in items:
            entry_id = str(item['id'])
            if entry_id in known_ids:
                n_known_items += 1
                continue

            """
            the item was not seen before
            """
            known_ids.add(entry_id)

            # -----------------------------------------------------------------
            # get tokens
            item['tokens'] = []
            if "topics" in item and item["topics"]:
                item['tokens'].extend([it['name'] for it in item["topics"]])
            item['tokens'].extend(ct.exclude_unknown_tokens(ct.get_tokens(
                str(item['title']) + ". " + str(item['abstract'])
            )))
            # /get tokens
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            # apply PTM
            item['ptm'] = list(ptm.topics_from_doc(item['tokens']))
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            # distance_to_seed
            if entry_id in seed_ids:
                item['distance_to_seed'] = 0
            else:
                print()
                all_distances = [
                    difference(item['ptm'], seed_items[seed_item_id]['ptm'])
                    for seed_item_id in seed_items
                ]
                print(all_distances)
                item['distance_to_seed'] = min(all_distances)
            # /distance_to_seed
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            # save seed to separate dictionary
            if entry_id in seed_ids:
                seed_items[entry_id] = item
            # -----------------------------------------------------------------

            item_is_valid = True
            for t in item['topics']:
                if t['id'] in exclude_topics:
                    item_is_valid = False

            if item_is_valid and item['distance_to_seed'] > max_distance:
                item_is_valid = False

            if item_is_valid:

                n_accepted_ids += 1
                json_batch.append(item)

                # -------------------------------------------
                # extend queue
                if entry_id not in done_ids and entry_id not in queued_ids_set:
                    queued_ids.put(entry_id)

                for related_entry_id in item['references_to']:
                    if related_entry_id not in done_ids and related_entry_id not in queued_ids_set:
                        queued_ids_set.add(related_entry_id)
                        queued_ids.put(related_entry_id)

                for related_entry_id in item['referenced_by']:
                    if related_entry_id not in done_ids and related_entry_id not in queued_ids_set:
                        queued_ids_set.add(related_entry_id)
                        queued_ids.put(related_entry_id)
                # /extend queue
                # -------------------------------------------
                msg = ("+++++accepted",
                       n_accepted_ids,
                       'of', len(known_ids),
                       "id", item['id'],
                       "dist", item['distance_to_seed'],
                       "citation_index=", item['citation_index'],
                       "year", item['year'],
                       "title", item['title'])
            else:
                msg = ("-----rejected",
                       n_accepted_ids,
                       'of', len(known_ids),
                       "id", item['id'],
                       "dist", item['distance_to_seed'],
                       "citation_index=", item['citation_index'],
                       "year", item['year'],
                       "title", item['title'])
            log(msg)

        
        log(('n_known_items', n_known_items))
        with jsonlines.open(file_path_output, mode='a') as writer:
            for item in json_batch:
                log(('id', item['id'], 'year', item['year'], 'title', item['title']))
                writer.write(item)

        if cnt >= save_period or n_known_items==len(items):
            """
                save current state
            """
            cnt = 0
            with open(file_path_queued_ids, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

                queued_ids_old = queued_ids
                queued_ids = queue.Queue()
                try:
                    while True:
                        entry_id = queued_ids_old.get_nowait()
                        writer.writerow([entry_id])
                        queued_ids.put(entry_id)
                except:
                    pass

            with open(file_path_done_ids, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for entry_id in done_ids:
                    writer.writerow([entry_id])

            with open(file_path_known_ids, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for entry_id in known_ids:
                    writer.writerow([entry_id])

            if len(done_ids) >= 20000 or n_known_items == len(items):
                break

        cnt += 1
    # /snowball loop
    # =====================================================

    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(snowball)

