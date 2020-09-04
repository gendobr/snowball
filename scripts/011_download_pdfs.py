# import sys
import os.path
import time
import fire
import configparser
import jsonlines
import urllib.request
import re


def do_extension(config=None, outfile=None, initems=None, pdfdir=None):
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

    pdf_dir = f'{data_dir}/pdfs'
    if pdfdir and os.path.isdir(pdfdir):
        pdf_dir = pdfdir
    elif os.path.isfile(pdf_dir):
        pass
    else:
        print(f'pdf dir {pdf_dir} not found')
        return
    print(('pdf_dir', pdf_dir))

    pdf_url_pattern = r'pdf$'
    for item_id in items:
        if 'pdf_present ' in items[item_id] and items[item_id]['pdf_present']:
            print(('item_id', item_id, 'skip'))
            continue
        # ======= download pdf = begin ==============
        # search url of the pdf file
        pdf_url = None
        if "google_scholar" in items[item_id] \
            and "eprint" in items[item_id]["google_scholar"]:
            pdf_url = items[item_id]["google_scholar"]["eprint"]
            if not re.search(pdf_url_pattern,pdf_url):
                pdf_url = None
        if pdf_url is None and 'urls' in items[item_id]:
            for u in items[item_id]['urls']:
                if pdf_url is None and "Ty" in u and u["Ty"] == 3:
                    pdf_url = u["U"]
                    if not re.search(pdf_url_pattern, pdf_url):
                        pdf_url = None

        # compose file name
        # > <Year>+”-“+<Type>+”-“+<Volume>+”(“+<Issue>+”)-(“+<Pages>+”)-“+(substring of <DOI> after ‘/’; all the <DOI> string if there is no ‘/’ in it)
        # > Year: Publication year, Column A
        # > Type: Publication type, Column B
        # > Volume: Volume No, Column E, 1 if not available
        # > Issue: Issue No, Column F, 1 if not available
        # > Pages: Column G
        # > DOI: Column H
        fn_year = items[item_id]["year"]
        fn_type = items[item_id]["publication_type"]
        fn_volume = items[item_id].get("volume") or 'null'
        fn_issue = items[item_id].get("issue") or 'null'
        fn_page_first = items[item_id].get("page_first") or 'null'
        fn_page_last = items[item_id].get("page_last") or 'null'
        fn_doi = re.sub(r'^[^/]+\/', '', (items[item_id].get("DOI") or 'null') )
        fn_uid = items[item_id].get("id")
        pdf_file_name = f"{fn_year}-{fn_type}-{fn_volume}({fn_issue})-({fn_page_first}-{fn_page_last})-({fn_doi})-({fn_uid}).pdf"
        pdf_file_path = f"{pdf_dir}/{pdf_file_name}"
        items[item_id]['pdf_file_name'] = pdf_file_name
        items[item_id]['pdf_present'] = False

        if pdf_url is None:
            print(('item_id', item_id, 'pdf_url', None))
            items[item_id]['pdf_url'] = ''
        else:
            # do download
            print(('item_id', item_id, 'pdf_url', pdf_url, 'pdf_file_path', pdf_file_path))
            items[item_id]['pdf_url'] = pdf_url
            try:
                urllib.request.urlretrieve(pdf_url, pdf_file_path)
                items[item_id]['pdf_present'] = True
                print(('item_id', item_id, 'status', 'success'))
            except:
                print(('item_id', item_id, 'status', 'error'))
        # ======= download pdf = end ================

    with jsonlines.open(file_path_output, mode='a') as writer:
        for item_id in items:
            item = items[item_id]
            print(('id', item['id'], 'pdf_present', items[item_id]['pdf_present'], 'pdf_file_name', item['pdf_file_name'], 'title', item['title']))
            writer.write(item)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(do_extension)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0,))
