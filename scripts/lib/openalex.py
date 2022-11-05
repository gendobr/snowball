
# import http.client as httplib
import json
import re
import urllib
from nltk.stem.porter import *
import os.path
import requests
from typing import List, Any, Union, Tuple, Dict
import traceback
import time



class Api:

    def __init__(self, include_topics):
        self.rest_endpoint = "https://api.openalex.org"
        self.include_topics = include_topics


    def load_by_ids(self, entry_ids, verbose=False):
        restrict_ids = "ids.openalex:" + ('|'.join([self.short_id(x) for x in entry_ids]))
        if len(self.include_topics)>0:
            restrict_topics = ",concepts.id:" + ("|".join([self.short_id(x) for x in self.include_topics]))
        else:
            restrict_topics = ""
        res = self.call_api(f"filter={restrict_ids}{restrict_topics}", verbose)
        return res


    def short_id(self, long_id):
        return str(long_id).removeprefix('https://openalex.org/')


    def load_by_rids(self, entry_ids, verbose=False):
        restrict_ids = "cites:" + ('|'.join([self.short_id(x) for x in entry_ids]))
        if len(self.include_topics)>0:
            restrict_topics = ",concepts.id:" + ("|".join([self.short_id(x) for x in self.include_topics]))
        else:
            restrict_topics = ""
        res = self.call_api(f"filter={restrict_ids}{restrict_topics}", verbose)
        return res


    def call_api(self, query, verbose=False):
        time.sleep(0.11)
        res = []
        url = f'{self.rest_endpoint}/works?{query}'
        print(url)
        r = requests.get(url)
        response = r.json()
        if verbose: print(f"url = '{url}'")
        try:
            entities = get_optional(['results'], response, [])
            # print(entities)
            for entity in entities:
                en = self.load_entity(entity)
                res.append(en)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        return res

    def load_entity(self, entity):
        res = Entry()

        res.raw = entity

        res.entryId = self.short_id(entity["id"])

        res.entryTitle = entity["title"]

        res.entryURL = entity["ids"]["openalex"]

        res.entryAbstract = ""
        inverted_index = get_optional(['abstract_inverted_index'], entity, {})

        max_position = 0
        for k in inverted_index:
            pos = max(inverted_index[k])
            if pos > max_position:
                    max_position = pos
        index_length = max_position + 1
        w = ["" for i in range(0, index_length)]
        for word in inverted_index:
            for pos in inverted_index[word]:
                w[pos] = word
        regex = re.compile(r"\n|\r", re.IGNORECASE)
        res.entryAbstract = regex.sub(" ", " ".join(w))

        res.entryPublished = entity.get("publication_year")

        res.authors = []
        raw_authors = get_optional(['authorships'], entity, [])

        for raw_author in raw_authors:
            a = Author()
            a.id = get_optional(['author', 'id'], raw_author, '')
            a.name = get_optional(['author', 'display_name'], raw_author, '')
            a.affiliation = get_optional(['institutions', 0, 'display_name'], raw_author, '')
            a.affiliationId = get_optional(['institutions', 0, 'id'], raw_author, '')
            res.authors.append(a)

        res.topics = []
        raw_topics = get_optional(['concepts'], entity, [])
        for raw_topic in raw_topics:
            t = Topic()
            t.topicId = get_optional(['id'], raw_topic, [])
            t.topicName = get_optional(['display_name'], raw_topic, [])
            t.raw = raw_topic
            res.topics.append(t)

        res.referencesTo = get_optional(['referenced_works'], entity, [])

        res.DOI = get_optional(['ids','doi'], entity, [])

        res.citation_index = get_optional(['cited_by_count'], entity, [])

        res_dict = res.to_json()


        # res_dict['bibtex_type'] = Api.BibTex_document_types.get(entity.get("BT"))
        res_dict['publication_type'] = get_optional(["type"], entity, [])
        res_dict['venue_full_name'] = get_optional(["host_venue", "display_name"], entity, [])
        res_dict['venue_short_name'] = res_dict['venue_full_name']
        res_dict['publisher'] = get_optional(["host_venue", "publisher"], entity, [])
        res_dict['volume'] = get_optional(["biblio", "volume"], entity, [])
        res_dict['issue'] = get_optional(["biblio", "issue"], entity, [])
        res_dict['page_first'] = get_optional(["biblio", "first_page"], entity, [])
        res_dict['page_last'] = get_optional(["biblio", "last_page"], entity, [])
        return res_dict

    # PUBLICATION_TYPE_MAP = {
    #     '0': 'UN',  # Unknown
    #     '1': 'JA',  # Journal article
    #     '2': 'PT',  # Patent
    #     '3': 'CP',  # Conference paper
    #     '4': 'BC',  # Book chapter
    #     '5': 'BO',  # Book
    #     '6': 'BR',  # Book reference entry
    #     '7': 'DA',  # Dataset
    #     '8': 'RE',  # Repository
    #     '': '',  #
    # }
    # BibTex_document_types = {
    #     'a': 'article',
    #     'b': 'book',
    #     'c': 'inbook',
    #     'p': 'inproceedings'
    # }




    def load_by_rids_extended(self, entry_ids, verbose=False):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["RId=" + regex.sub('', str(x)) for x in entry_ids])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in self.include_topics])) + ")"
        return self.call_api("and(" + sbIds + ", " + sbFIds + ")", ','.join(Api.FIELDS), verbose)
    
    def loadList(self, f):
        q = []
        
        #out-invalid.csv
        if os.path.isfile(f) :
            thefile = open(f, 'r')
            data = thefile.read()
            thefile.close();

            a = data.split("\n")
            for row in a:
                rw = row.strip(" \n\t")
                if len(rw) > 0:    
                    tmp = rw.split("#")
                    q.append(tmp[0].strip(" \t"))
        return q


    def loadEntries(self, f):
        q = []
        thefile = open(f, 'r')
        data = thefile.read()
        thefile.close();

        a = data.split("\n")
        for row in a:
            if len(row) > 0:
                q.append(entryFromCsv(row.strip(' ')))
        return q



    def saveList(self, file, ids):
        thefile = open(file, 'w')
        thefile.write("\n".join([str(i) for i in ids]))
        thefile.close();

    def saveEntries(self, file, entries):
        thefile = open(file, 'w')
        for entry in entries:
            thefile.write(entry.toCsv())
            thefile.write("\n")
        thefile.close();


def get_optional(
    path: List[Any],
    tree: Union[List[Any], Tuple[Any], Dict[Any, Any]],
    default_value=None,
) -> Any:
    """
    Extract branch from tree using path
    """
    if tree is None:
        return default_value
    res = tree
    for p in path:
        try:
            res = res[p]
        except (TypeError, IndexError, KeyError):
            return default_value
    if res is None:
        return default_value
    return res


class Entry:
    def __init__(self):
        self.entryId = ''
        self.entryTitle = ''
        self.entryURL = ''
        self.entryAbstract = ''
        self.entryPublished = ''
        self.authors = []
        self.topics = []
        self.referencesTo = []
        self.referencedBy = []
        self.level = ''
        self.citation_index = 0
        self.DOI =''
        self.raw = {}

    def to_json(self):
        _d = dict(
            id=self.entryId,
            title=self.entryTitle,
            url=self.entryURL,
            abstract=self.entryAbstract,
            year=self.entryPublished,
            authors=[a.to_json() for a in self.authors],
            topics=[a.to_json() for a in self.topics],
            references_to=self.referencesTo,
            referenced_by=self.referencedBy,
            level=self.level,
            citation_index=self.citation_index,
            doi=self.DOI,
            raw=self.raw
        )
        return _d


class Topic:

    def __init__(self):
        self.topicId = ''
        self.topicName = ''
        self.raw = {}

    def to_json(self):
        _d = dict(
            id=self.topicId,
            name=self.topicName,
            raw=self.raw,
        )
        return _d


class Author:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.affiliation = ''
        self.affiliationId = ''
        self.raw = {}

    def to_json(self):
        _d = dict(
            id=self.id,
            name=self.name,
            affiliation=self.affiliation,
            affiliationId=self.affiliationId,
            raw=self.raw
        )
        return _d


