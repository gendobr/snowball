# import sys
import os.path
import time
import fire
import configparser
import jsonlines
import psutil
import scholarly
import sys


def do_extension(config=None, outfile=None, initems=None, searchauthor='1', searchtitle='1', searchvenue='0'):
    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get('main', 'data_dir')

    # =====================================================
    # place to store extended item
    if outfile:
        file_path_output = outfile
    else:
        file_path_output = f'{data_dir}/010_extend_items_google_scholar.jsonl'
    print(('output', file_path_output))
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
        print('input file not found')
        return
    print(('infile', file_path_items))
    with jsonlines.open(file_path_items) as reader:
        items = {str(row['id']): row for row in reader}
    # /load downloaded items
    # =====================================================

    # place here Google Scholar calls to extract citation index
    # ! maybe proxy is needed
    proxy = conf.get('google_scholar', 'proxy')
    scholarly.scholarly.use_proxy(http=proxy)

    n_errors = 0
    for item_id in items:

        print(('extending', 'item_id', item_id))

        if 'google_scholar' in items[item_id]:
            print(('skip', 'item_id', item_id, ))
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
            print(('searching', 'google_search_string', google_search_string, ))
            try:
                search_query = scholarly.scholarly.search_pubs(google_search_string)
                pub = next(search_query)
                items[item_id]['google_scholar'] = dict(
                    abstract=pub.bib['abstract'],
                    author=pub.bib['author'],
                    cites=pub.bib['cites'],
                    eprint=pub.bib['eprint'],
                    gsrank=pub.bib['gsrank'],
                    title=pub.bib['title'],
                    url=pub.bib['url'],
                    venue=pub.bib['venue'],
                    year=pub.bib['year'],
                    bibtex=pub.bibtex,
                )
                print(items[item_id]['google_scholar'])
                n_errors = 0
            except:
                n_errors += 1
                print("ERROR", sys.exc_info()[0])
                if n_errors > 10:
                    __save_items(file_path_output, items)
                    break
        else:
            print('ERROR', 'message', 'google_search_string is empty')

    __save_items(file_path_output, items)


def __save_items(file_path_output, items):
    with jsonlines.open(file_path_output, mode='a') as writer:
        for item_id in items:
            item = items[item_id]
            print(('id', item['id'], 'year', item['year'], 'title', item['title']))
            writer.write(item)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_extension)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
    process = psutil.Process(os.getpid())
    print('used RAM(bytes)=', process.memory_info().rss)  # in bytes