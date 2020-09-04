
import scholarly
import time
import fire
import configparser
import json
from fp.fp import FreeProxy


def set_new_proxy():
    while True:
        proxy = FreeProxy(rand=True, timeout=1).get()
        print(('try', 'proxy', proxy))
        proxy_works = scholarly.scholarly.use_proxy(http=proxy, https=proxy)
        if proxy_works:
            break
    print("Working proxy:", proxy)
    return proxy


def main(config=None):
    # read configuration file
    conf = configparser.ConfigParser()
    # conf.readfp(open(dir+'/config.ini'))
    conf.read_file(open(config))

    proxy = conf.get('google_scholar', 'proxy')
    print(('proxy', proxy,))

    # set_new_proxy()
    proxy_connected = scholarly.scholarly.use_proxy(http=proxy, https=proxy)
    print(('proxy_connected', proxy_connected))

    # search_query = scholarly.scholarly.search_pubs('Perception of physical stability and center of mass of 3D objects')
    search_query = scholarly.scholarly.search_pubs('''allintitle: Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals author:"J Gray" source:"Data Mining and Knowledge Discovery"''')
    pub = next(search_query)
    print(pub)
    print("++++++++++++++++++++++++")
    # print(res)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(main)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0, ))

'''
response 1:
{'bib': {'abstract': 'Humans can judge from vision alone whether an object is '
                     'physically stable or not. Such judgments allow observers '
                     'to predict the physical behavior of objects, and hence '
                     'to guide their motor actions. We investigated the visual '
                     'estimation of physical stability of 3-D objects (shown '
                     'in stereoscopically viewed rendered scenes) and how it '
                     'relates to visual estimates of their center of mass '
                     '(COM). In Experiment 1, observers viewed an object near '
                     'the edge of a table and adjusted its tilt to the '
                     'perceived critical angle, ie, the tilt angle at which '
                     'the object',
         'author': ['SA Cholewiak', 'RW Fleming', 'M Singh'],
         'cites': '23',
         'eprint': 'https://jov.arvojournals.org/article.aspx?articleID=2213254',
         'gsrank': '1',
         'title': 'Perception of physical stability and center of mass of 3-D '
                  'objects',
         'url': 'https://jov.arvojournals.org/article.aspx?articleID=2213254',
         'venue': 'Journal of vision',
         'year': '2015'},
 'citations_link': '/scholar?cites=15736880631888070187&as_sdt=5,33&sciodt=0,33&hl=en',
 'filled': False,
 'source': 'scholar',
 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DPerception%2Bof%2Bphysical%2Bstability%2Band%2Bcenter%2Bof%2Bmass%2Bof%2B3D%2Bobjects%26hl%3Den%26as_sdt%3D0,33&citilm=1&json=&update_op=library_add&info=K8ZpoI6hZNoJ&ei=xptPX_yZA7OD6rQPpsuL8Ao',
 'url_scholarbib': '/scholar?q=info:K8ZpoI6hZNoJ:scholar.google.com/&output=cite&scirp=0&hl=en'}
 
response 2:
{'bib': {'abstract': 'Data analysis applications typically aggregate data '
                     'across manydimensions looking for anomalies or unusual '
                     'patterns. The SQL aggregatefunctions and the GROUP BY '
                     'operator produce zero-dimensional orone-dimensional '
                     'aggregates. Applications need the '
                     'N-dimensionalgeneralization of these operators. This '
                     'paper defines that operator, calledthe data cube or '
                     'simply cube. The cube operator generalizes the '
                     'histogram, cross-tabulation, roll-up, drill-down, and '
                     'sub-total constructs found in most report writers. The '
                     'novelty is that',
         'author': ['J Gray', 'S Chaudhuri', 'A Bosworth', 'A Layman'],
         'cites': '3411',
         'eprint': 'https://arxiv.org/pdf/cs/0701155',
         'gsrank': '1',
         'title': 'Data cube: A relational aggregation operator generalizing '
                  'group-by, cross-tab, and sub-totals',
         'url': 'https://link.springer.com/article/10.1023/A:1009726021843',
         'venue': 'Data mining and …',
         'year': '1997'},
 'citations_link': '/scholar?cites=10836794633940449959&as_sdt=5,33&sciodt=0,33&hl=en',
 'filled': False,
 'source': 'scholar',
 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Dallintitle:%2BData%2BCube:%2BA%2BRelational%2BAggregation%2BOperator%2BGeneralizing%2BGroup-By,%2BCross-Tab,%2Band%2BSub-Totals%2Bauthor:%2522J%2BGray%2522%2Bsource:%2522Data%2BMining%2Band%2BKnowledge%2BDiscovery%2522%26hl%3Den%26as_sdt%3D0,33&citilm=1&json=&update_op=library_add&info=pzrhw00HZJYJ&ei=bp1PX_LALsacywS1kLjIDQ',
 'url_scholarbib': '/scholar?q=info:pzrhw00HZJYJ:scholar.google.com/&output=cite&scirp=0&hl=en'}

'''

