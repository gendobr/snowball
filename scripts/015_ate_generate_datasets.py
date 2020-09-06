import fire
import configparser
import psutil
import lib.datasetfactory as dsf
import time
import os


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
    :param strategy: time-asc | time-desc | random | time-bidir | citation-desc
    :return:
    """
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    # =====================================================
    # place to store extracted texts
    if cleartxtdir:
        clear_txt_dir = cleartxtdir
    else:
        clear_txt_dir = f'{data_dir}/clear_txts'
    print(('clear_txt_dir', clear_txt_dir))
    # =====================================================

    # =====================================================
    # place to read raw texts
    if datasetdir:
        out_dataset_dir = datasetdir
    else:
        out_dataset_dir = f'{data_dir}/datasets'
    print(('raw_txt_dir', out_dataset_dir))
    # =====================================================

    print("reading raw TXT from", cleartxtdir, "writing datasets to", out_dataset_dir)

    if strategy == 'citation-desc':
        dsf.factory_citation_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'citation-per-year-desc':
        dsf.factory_citation_per_year_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'spc-desc':
        dsf.factory_spc_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size,
                                       metadata=metadatafile)
    elif strategy == 'time-desc':
        dsf.factory_time_desc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'time-asc':
        dsf.factory_time_asc(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'time-bidir':
        dsf.factory_time_bidir(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
    elif strategy == 'random':
        dsf.factory_random(clear_txt_dir, out_dataset_dir, increment_size=increment_size, metadata=metadatafile)
#

if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_generate_datasets)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    print('used RAM(bytes)=', process.memory_info().rss)  # in bytes