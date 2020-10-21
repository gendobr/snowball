# import PyPDF2
from os import listdir
import pandas as pd
from os.path import isfile
from os.path import join
import datetime
import random
import time
import jsonlines
import json
import re





def partial_factory_citation_per_year_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_citation_per_year_desc(txt_file_dir, metadata=metadata)
    __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def partial_factory_citation_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_citation_desc(txt_file_dir, metadata=metadata)
    __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def partial_factory_spc_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_spc_desc(txt_file_dir, metadata=metadata)
    __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def partial_factory_time_bidir(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_time_bidir(txt_file_dir, metadata=metadata)
    __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def partial_factory_random(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    pairs = __sort_random(txt_file_dir, metadata=metadata)
    __create_partial_datasets(pairs, increment_size, dataset_file_dir)


def partial_factory_time_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_time_desc(txt_file_dir, metadata=metadata)
    __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def partial_factory_time_asc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_time_asc(txt_file_dir, metadata=metadata)
    __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def factory_citation_per_year_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_citation_per_year_desc(txt_file_dir, metadata=metadata)
    __create_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def factory_citation_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_citation_desc(txt_file_dir, metadata=metadata)
    __create_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def factory_spc_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_spc_desc(txt_file_dir, metadata=metadata)
    __create_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def factory_time_bidir(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_time_bidir(txt_file_dir, metadata=metadata)
    __create_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def factory_random(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    pairs = __sort_random(txt_file_dir, metadata=metadata)
    __create_datasets(pairs, increment_size, dataset_file_dir)


def factory_time_desc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_time_desc(txt_file_dir, metadata=metadata)
    __create_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def factory_time_asc(txt_file_dir, dataset_file_dir, increment_size=1, metadata=False):
    sorted_txt_files = __sort_time_asc(txt_file_dir, metadata=metadata)
    __create_datasets(sorted_txt_files, increment_size, dataset_file_dir)


def __sort_citation_per_year_desc(txt_file_dir, metadata=False):
    t0 = time.time()
    # read metadata file
    if metadata[-6:] == '.jsonl':
        with jsonlines.open(metadata) as reader:
            items = {str(row['id']): row for row in reader}

        now_year = datetime.datetime.utcnow().year

        # get pairs (citation_index, file_path)
        pairs = []
        for item_id in items:
            item = items[item_id]
            txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
            if isfile(txt_file_path):
                citations_per_year = 0
                try:
                    order_by = int(item["google_scholar"]["cites"]) / (now_year - int(item["year"]) + 1)
                except:
                    order_by = 0
                pairs.append((order_by, txt_file_path,))
    elif metadata[-5:] == '.xlsx':
        items = json.loads(pd.read_excel(metadata).to_json(orient="records"))
        pairs = []
        for item in items:
            order_by = item["Citations per year (GS)"]
            txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["Document file name"]))
            if isfile(txt_file_path):
                pairs.append((order_by, txt_file_path,))

    sorted_txt_files = sorted(pairs, reverse=True)
    # print(sorted_txt_files)
    return sorted_txt_files


def __sort_citation_desc(txt_file_dir, metadata=False):
    t0 = time.time()
    # read metadata file
    with jsonlines.open(metadata) as reader:
        items = {str(row['id']): row for row in reader}

    # get pairs (citation_index, file_path)
    pairs = []
    for item_id in items:
        item = items[item_id]
        txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
        if isfile(txt_file_path):
            try:
                order_by = int(item["google_scholar"]["cites"])
            except:
                order_by = 0
            pairs.append((order_by, txt_file_path,))

    sorted_txt_files = sorted(pairs, reverse=True)
    # print(sorted_txt_files)
    return sorted_txt_files


def __sort_spc_desc(txt_file_dir, metadata=False):
    t0 = time.time()
    # read metadata file
    with jsonlines.open(metadata) as reader:
        items = {str(row['id']): row for row in reader}

    # get pairs (citation_index, file_path)
    pairs = []
    for item_id in items:
        item = items[item_id]
        txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
        if isfile(txt_file_path):
            try:
                order_by = float(item["spc"])
            except:
                order_by = 0
            pairs.append((order_by, txt_file_path,))

    sorted_txt_files = sorted(pairs, reverse=True)
    # print(sorted_txt_files)
    return sorted_txt_files


def __sort_time_bidir(txt_file_dir, metadata=False):
    t0 = time.time()
    # read metadata file
    with jsonlines.open(metadata) as reader:
        items = {str(row['id']): row for row in reader}

    # get pairs (citation_index, file_path)
    pairs = []
    for item_id in items:
        item = items[item_id]
        txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
        if isfile(txt_file_path):
            try:
                order_by = int(item["google_scholar"]["cites"])
            except:
                order_by = 0
            pairs.append((order_by, txt_file_path,))

    n_files = len(pairs)
    i_max = int(len(pairs) / 2)
    sorted_txt_files = []
    for i1 in range(0, i_max):
        sorted_txt_files.append(pairs[i1])
        i2 = n_files - i1 - 1
        sorted_txt_files.append(pairs[i2])
    # print(sorted_txt_files)
    return sorted_txt_files


def __sort_random(txt_file_dir, metadata=False):

    t0 = time.time()
    # read metadata file
    with jsonlines.open(metadata) as reader:
        items = {str(row['id']): row for row in reader}

    # get pairs (citation_index, file_path)
    pairs = []
    for item_id in items:
        item = items[item_id]
        txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
        if isfile(txt_file_path):
            try:
                order_by = int(item["google_scholar"]["cites"])
            except:
                order_by = 0
            pairs.append((order_by, txt_file_path,))

    random.shuffle(pairs)
    # print(pairs)
    return pairs


def __sort_time_desc(txt_file_dir, metadata=False):
    t0 = time.time()
    # read metadata file
    with jsonlines.open(metadata) as reader:
        items = {str(row['id']): row for row in reader}

    # get pairs (citation_index, file_path)
    pairs = []
    for item_id in items:
        item = items[item_id]
        txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
        if isfile(txt_file_path):
            try:
                order_by = -int(item["year"])
            except:
                order_by = 0
            pairs.append((order_by, txt_file_path,))

    sorted_txt_files = sorted(pairs)
    # print(sorted_txt_files)
    return sorted_txt_files


def __sort_time_asc(txt_file_dir, metadata=False):
    t0 = time.time()
    # read metadata file
    with jsonlines.open(metadata) as reader:
        items = {str(row['id']): row for row in reader}

    # get pairs (citation_index, file_path)
    pairs = []
    for item_id in items:
        item = items[item_id]
        txt_file_path = join(txt_file_dir, re.sub(r'\.pdf$', '.txt', item["pdf_file_name"]))
        if isfile(txt_file_path):
            try:
                order_by = int(item["year"])
            except:
                order_by = 0
            pairs.append((order_by, txt_file_path,))

    sorted_txt_files = sorted(pairs)
    # print(sorted_txt_files)
    return sorted_txt_files




def __create_datasets(sorted_txt_files, increment_size, dataset_file_dir):
    t0 = time.time()
    dataset = ''
    n_dataset = 0
    for chunk in __get_chunks(sorted_txt_files, increment_size):
        n_dataset += 1
        for pair in chunk:
            with open(pair[1]) as fl:
                dataset += fl.read()
        fnm = join(dataset_file_dir, 'D' + (('00000000000000000' + str(n_dataset))[-10:]) + '.txt')
        fl = open(fnm, 'w')
        fl.write(dataset)
        fl.close()
        t1 = time.time()
        print(n_dataset, fnm, t1 - t0, 'sec', chunk)
        print("\n")


def __create_partial_datasets(sorted_txt_files, increment_size, dataset_file_dir):
    t0 = time.time()
    n_dataset = 0
    for chunk in __get_chunks(sorted_txt_files, increment_size):
        n_dataset += 1
        dataset = ''
        for pair in chunk:
            with open(pair[1]) as fl:
                dataset += fl.read()
        fnm = join(dataset_file_dir, 'D' + (('00000000000000000' + str(n_dataset))[-10:]) + '.txt')
        fl = open(fnm, 'w')
        fl.write(dataset)
        fl.close()
        t1 = time.time()
        print(n_dataset, fnm, t1 - t0, 'sec', chunk)
        print("\n")


def __get_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

