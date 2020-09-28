import fire
import configparser
import psutil
import lib.datasetfactory as dsf
import time
import os, json


def do_generate_datasets(config=None,
                         datasetdir=None,
                         cleartxtdir=None,
                         increment_size=20,
                         metadatafile=None,
                         strategy='citation-desc'):
    """

    :param config:
    :param datasetdir:
    :param cleartxtdir:
    :param increment_size:
    :param strategy: citation-desc|citation-per-year-desc|spc-desc|time-desc|time-asc|time-bidir|random
                    |partial-citation-desc|partial-citation-per-year-desc|partial-spc-desc
                    |partial-time-desc|partial-time-asc|partial-time-bidir|partial-random
    :return:
    """
    t0 = time.time()

    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    log_file_name = '015_ate_generate_datasets.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # =====================================================
    # place to read extracted texts
    if cleartxtdir:
        clear_txt_dir = cleartxtdir
    else:
        clear_txt_dir = f'{data_dir}/clear_txts'
    log(('clear_txt_dir', clear_txt_dir))
    # =====================================================

    # =====================================================
    # place to store datasets
    if datasetdir:
        out_dataset_dir = datasetdir
    else:
        out_dataset_dir = f'{data_dir}/datasets'

    if not os.path.isdir(out_dataset_dir):
        log(f'pdf dir {out_dataset_dir} not found. Creating')
        os.mkdir(out_dataset_dir)

    log(('raw_txt_dir', out_dataset_dir))
    # =====================================================

    log(("reading raw TXT from", cleartxtdir, "writing datasets to", out_dataset_dir))

    if strategy == 'citation-desc':
        dsf.factory_citation_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'citation-per-year-desc':
        dsf.factory_citation_per_year_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'spc-desc':
        dsf.factory_spc_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'time-desc':
        dsf.factory_time_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'time-asc':
        dsf.factory_time_asc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'time-bidir':
        dsf.factory_time_bidir(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'random':
        dsf.factory_random(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-citation-desc':
        dsf.partial_factory_citation_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-citation-per-year-desc':
        dsf.partial_factory_citation_per_year_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-spc-desc':
        dsf.partial_factory_spc_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-time-desc':
        dsf.partial_factory_time_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-time-asc':
        dsf.partial_factory_time_asc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-time-bidir':
        dsf.partial_factory_time_bidir(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'partial-random':
        dsf.partial_factory_random(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)

    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


if __name__ == "__main__":
    fire.Fire(do_generate_datasets)
