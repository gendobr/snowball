#!/usr/bin/env python2
# encoding: UTF-8

# import sys
import os.path
from lib.msacademic import Api
import time
import fire
import configparser
import json
import jsonlines
import csv
import queue


def snowball(config=None, outfile=None, infile=None):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    rest_endpoint = json.loads(conf.get('msacademic', 'restEndpoint'))
    subscription_key = conf.get('msacademic', 'subscriptionKey')
    include_topics = json.loads(conf.get('msacademic', 'msAcademicIncludeTopicsIds'))

    api = Api(subscription_key, rest_endpoint, include_topics)

    data_dir = conf.get('main', 'data_dir')

    # file names
    file_path_queued_ids = f'{data_dir}/000_download_queued_ids.csv'
    file_path_known_ids = f'{data_dir}/000_download_known_ids.csv'
    file_path_done_ids = f'{data_dir}/000_download_done_ids.csv'
    file_path_seed_ids = f'{data_dir}/in-seed.csv'

    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/000_download_output.jsonl'
    print(('output', file_path_output))

    if infile and infile == 'resume' and os.path.isfile(file_path_queued_ids):
        file_path_initial_queued_ids = file_path_queued_ids
    elif infile and os.path.isfile(infile):
        file_path_initial_queued_ids = infile
    else:
        file_path_initial_queued_ids = file_path_seed_ids
    print(('input', file_path_initial_queued_ids))

    # =====================================================
    # load initial ids to queue
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
    # load done ids
    done_ids = set()
    if os.path.isfile(file_path_done_ids):
        with open(file_path_done_ids, newline='') as csvfile:
            queue_reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            for row in queue_reader:
                item_id = str(row[0])
                queued_ids_set.add(item_id)
                done_ids.add(item_id)
    # /load done ids
    # =====================================================

    # =====================================================
    # load known ids
    known_ids = set()
    if os.path.isfile(file_path_known_ids):
        with open(file_path_known_ids, newline='') as csvfile:
            queue_reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            for row in queue_reader:
                known_ids.add(str(row[0]))
    # /load done ids
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
        try:
            while len(next_batch_ids) < batch_size:
                next_id = queued_ids.get_nowait()
                if next_id not in done_ids:
                    next_batch_ids.append(next_id)
        except:
            pass

        if len(next_batch_ids) == 0:
            break

        done_ids.update(next_batch_ids)

        items = api.load_by_ids(next_batch_ids)
        items.extend(api.load_by_rids(next_batch_ids))
        api_call_counter += 2
        print(('api_call_counter', api_call_counter, 'queue_size', queued_ids.qsize()))
        for item in items:
            entry_id = str(item['id'])
            if entry_id in known_ids:
                continue

            json_batch.append(item)
            known_ids.add(entry_id)

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
        with jsonlines.open(file_path_output, mode='a') as writer:
            for item in json_batch:
                print(('id', item['id'], 'year', item['year'], 'title', item['title']))
                writer.write(item)

        if cnt >= save_period:
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

        cnt += 1
    # /snowball loop
    # =====================================================


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(snowball)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
