# import sys
import os.path
import time
import fire
import configparser
import jsonlines
import psutil
import scholarly
import sys, traceback, random, json


def do_extension(config=None, outfile=None, initems=None, searchauthor='1', searchtitle='1', searchvenue='0'):
    t0 = time.time()

    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')
    log_file_name = '010_extend_items_google_scholar.log'
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # =====================================================
    # place to store extended item
    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/010_extend_items_google_scholar.jsonl'
    log(('output', file_path_output))
    # =====================================================

    # =====================================================
    # load downloaded items
    file_path_items = f'{data_dir}/009_extend_items_output.jsonl'
    if initems and initems == 'resume':
        file_path_items = file_path_output
    elif initems and os.path.isfile(initems):
        file_path_items = initems
    elif os.path.isfile(file_path_items):
        pass
    else:
        log('input file not found')
        return
    log(('infile', file_path_items))
    with jsonlines.open(file_path_items) as reader:
        items = {str(row['id']): row for row in reader}
    # /load downloaded items
    # =====================================================

    # place here Google Scholar calls to extract citation index
    # ! maybe proxy is needed
    proxy = conf.get('google_scholar', 'proxy')
    if len(proxy) > 0:
        scholarly.scholarly.use_proxy(http=proxy)

    scholarly.scholarly.set_retries(1)

    n_errors = 0
    for item_id in items:

        log(('extending', 'item_id', item_id))

        if 'google_scholar' in items[item_id]:
            log(('skip', 'item_id', item_id, ))
            continue

        google_search_string = list()
        if searchtitle == '1':
            try:
                item_title = items[item_id]["title"]
                google_search_string.append(f'''allintitle: {item_title}''')
            except:
                pass

        if searchauthor == '1':
            try:
                item_author = items[item_id]["authors"][0]["name"]
                google_search_string.append(f'''author:"{item_author}"''')
            except:
                pass

        if searchvenue == '1':
            try:
                item_venue = items[item_id]["venue_full_name"]
                google_search_string.append(f'''source:"{item_venue}"''')
            except:
                pass

        if len(google_search_string) > 0:
            google_search_string = " ".join(google_search_string)
            log(('searching', 'google_search_string', google_search_string, ))
            try:
                search_query = scholarly.scholarly.search_pubs(google_search_string)
                pub = next(search_query)
                items[item_id]['google_scholar'] = dict(
                    abstract=pub.bib['abstract'] if 'abstract' in pub.bib else '',
                    author=pub.bib['author'] if 'author' in pub.bib else '',
                    cites=pub.bib['cites'] if 'cites' in pub.bib else '',
                    eprint=pub.bib['eprint'] if 'eprint' in pub.bib else '',
                    gsrank=pub.bib['gsrank'] if 'gsrank' in pub.bib else '',
                    title=pub.bib['title'] if 'title' in pub.bib else '',
                    url=pub.bib['url'] if 'url' in pub.bib else '',
                    venue=pub.bib['venue'] if 'venue' in pub.bib else '',
                    year=pub.bib['year'] if 'year' in pub.bib else '',
                    bibtex=pub.bibtex,
                )
                log(items[item_id]['google_scholar'])
                n_errors = 0
                time.sleep((30-5)*random.random()+5) #from 5 to 30 seconds
            except:
                n_errors += 1
                ex = sys.exc_info()
                log(("ERROR", str(ex[0]), str(ex[1]), str(ex[2])))
                traceback.print_exc(file=sys.stdout)
                if n_errors > 10:
                    __save_items(file_path_output, items)
                    break
        else:
            log(('ERROR', 'message', 'google_search_string is empty'))

    __save_items(file_path_output, items)
    for item_id in items:
        item = items[item_id]
        log(('id', item['id'], 'year', item['year'], 'title', item['title']))

    t1 = time.time()
    log("finished")
    log(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    log(('used RAM(bytes)=', process.memory_info().rss))  # in bytes


def __save_items(file_path_output, items):
    with jsonlines.open(file_path_output, mode='w') as writer:
        for item_id in items:
            item = items[item_id]
            writer.write(item)


if __name__ == "__main__":
    fire.Fire(do_extension)
