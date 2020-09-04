
import http.client as httplib
import json
import re
import urllib
from nltk.stem.porter import *
import os.path


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
        self.ECC = 0

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
            ecc=self.ECC
        )
        return _d


class Topic:

    def __init__(self):
        self.topicId = ''
        self.topicName = ''

    def to_json(self):
        _d = dict(
            id=self.topicId,
            name=self.topicName,
        )
        return _d


class Author:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.affiliation = ''
        self.affiliationId = ''

    def to_json(self):
        _d = dict(
            id=self.id,
            name=self.name,
            affiliation=self.affiliation,
            affiliationId=self.affiliationId,
        )
        return _d


class Api:

    FIELDS = ['Id', 'Ti', 'Y', 'RId', 'F.FN', 'F.FN', 'F.FId', 'AA.AuId', 'AA.AuN', 'AA.AfN', 'AA.AfId', 'ECC']
    PUBLICATION_TYPE_MAP = {
        '0': 'UN',  # Unknown
        '1': 'JA',  # Journal article
        '2': 'PT',  # Patent
        '3': 'CP',  # Conference paper
        '4': 'BC',  # Book chapter
        '5': 'BO',  # Book
        '6': 'BR',  # Book reference entry
        '7': 'DA',  # Dataset
        '8': 'RE',  # Repository
        '': '',  #
    }
    BibTex_document_types = {
        'a': 'article',
        'b': 'book',
        'c': 'inbook',
        'p': 'inproceedings'
    }

    def __init__(self, subscription_key, rest_endpoint, include_topics):
        self.subscription_key = subscription_key
        self.rest_endpoint = rest_endpoint
        self.include_topics = include_topics

    def load_by_ids(self, entry_ids, verbose=False):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["Id=" + regex.sub('', str(int(x))) for x in entry_ids])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in self.include_topics])) + ")"
        res = self.call_api("and(" + sbIds + ", " + sbFIds + ")", ','.join(Api.FIELDS), verbose)
        #,E
        return res

    def load_by_rids(self, entry_ids, verbose=False):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["RId=" + regex.sub('', str(x)) for x in entry_ids])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in self.include_topics])) + ")"
        return self.call_api("and(" + sbIds + ", " + sbFIds + ")", ','.join(Api.FIELDS), verbose)

    def load_by_rids_extended(self, entry_ids, verbose=False):
        regex = re.compile(r"\\D", re.IGNORECASE)
        sbIds = "or(" + (','.join(["RId=" + regex.sub('', str(x)) for x in entry_ids])) + ")"
        sbFIds = "or(" + (",".join(["Composite(F.FId=" + regex.sub('', str(id)) + ")" for id in self.include_topics])) + ")"
        return self.call_api("and(" + sbIds + ", " + sbFIds + ")", ','.join(Api.FIELDS), verbose)

    def call_api(self, expr, attributes, verbose=False):
        res = []
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        if verbose: print("self.subscriptionKey=" + self.subscription_key + ';')
        # print expr
        params = urllib.parse.urlencode({
            # Request parameters
            'expr': expr,
            'complete': '0',
            'count': '1000',
            'offset': '0',
            'timeout': '60',
            'model': 'latest',
            'attributes': attributes
        })
        # print params

        try:
            if verbose:
                print(self.rest_endpoint)
            if verbose:
                print(params)

            conn = httplib.HTTPSConnection(self.rest_endpoint["host"])
            conn.request("GET", self.rest_endpoint["path"] + "?" + params, "", headers)
            response = conn.getresponse()
            if verbose:
                print(response.status, response.reason)
            json_string = response.read()
            if verbose:
                print(json_string)
            data = json.loads(json_string)
            if verbose:
                print(data)

            for entity in data['entities']:
                en = self.load_entity(entity)
                res.append(en)
            # print(data)
            conn.close()
        except Exception as e:
            # print("[Errno {0}] {1}".format(e.errno, e.strerror))
            print(e)

        return res

    def load_entity(self, entity):
        res = Entry()
        # "entities":
        # [
        # {
        #  "logprob":-15.670,
        #  "Id":2001082470,
        #  "Ti":"finding scientific topics",
        #  "Y":2004,
        #  "RId":[1574901103,33994038,1666636243,2069739265,2104924585,2534302,204170073,2165554837],
        #  "AA":[{"AuN":"thomas l griffiths","AuId":2122351653},
        #        {"AuN":"mark steyvers","AuId":499903789}],
        #  "F":[{"FN":"dynamic topic model","FId":181389423},
        #       {"FN":"topic model","FId":171686336},
        #	   {"FN":"documentation","FId":56666940},
        #	   {"FN":"latent dirichlet allocation","FId":500882744},
        #	   {"FN":"publishing","FId":151719136},
        #	   {"FN":"probability","FId":104396909},
        #	   {"FN":"monte carlo method","FId":19499675}
        #  ]}]
        # }
        #    public String entryId;
        res.entryId = entity["Id"]

        res.entryTitle = entity["Ti"]

        # public String entryURL;
        res.entryURL = "https://academic.microsoft.com/#/detail/" + str(res.entryId)

        res.entryAbstract = ""
        if "E" in entity:
            ex = json.loads(entity["E"])
            if "IA" in ex:
                regex = re.compile(r"\n|\r", re.IGNORECASE)
                ia = ex["IA"]
                index_length = ia["IndexLength"]
                inverted_index = ia["InvertedIndex"]
                w = ["" for i in range(0, index_length)]
                for word in inverted_index.keys():
                    for pos in inverted_index[word]:
                        w[pos] = word
                res.entryAbstract = regex.sub(" ", " ".join(w))

        if "Y" in entity:
            res.entryPublished = entity["Y"]
        else:
            res.entryPublished = None



        res.authors = []
        if "AA" in entity:
            for author in entity['AA']:
                a = Author()
                a.id = author["AuId"]
                a.name = author["AuN"]

                if "AfN" in author:
                    a.affiliation = author["AfN"]
                else:
                    a.affiliation = None

                if "AfId" in author:
                    a.affiliationId = author["AfId"]
                else:
                    a.affiliationId = None

                res.authors.append(a)

        res.topics = []
        if "F" in entity:
            for topic in entity["F"]:
                t = Topic()
                t.topicId = topic["FId"]
                t.topicName = topic["FN"]
                res.topics.append(t)

        res.referencesTo = []
        if "RId" in entity:
            for rid in entity["RId"]:
                res.referencesTo.append(rid)

        res_dict = res.to_json()

        res.ECC = int(entity["ECC"]) if "ECC" in entity else None

        # 'BT',  # BibTex document type ('a':Journal article, 'b':Book, 'c':Book chapter, 'p':Conference paper)
        res_dict['bibtex_type'] = Api.BibTex_document_types.get(entity.get("BT"))

        # 'Pt',  # Publication type (0:Unknown, 1:Journal article, 2:Patent, 3:Conference paper, 4:Book chapter,
        #                            5:Book, 6:Book reference entry, 7:Dataset, 8:Repository
        res_dict['publication_type'] = Api.PUBLICATION_TYPE_MAP.get(entity.get("Pt"))

        # 'VFN',  # Full name of the Journal or Conference venue    String    None
        res_dict['venue_full_name'] = entity.get("VFN")

        # 'VSN',  # Short name of the Journal or Conference venue    String    None
        res_dict['venue_short_name'] = entity.get("VSN")

        # 'J.JN',  # Journal name    String    Equals, StartsWith
        if "J" in entity:
            res_dict['journal_name'] = entity['J'].get('JN')

        # 'BV',  # BibTex venue name    String    None
        res_dict['bibtex_venue_name'] = entity.get("BV")

        # 'C.CN',  # Conference series name    String    Equals, StartsWith
        if "C" in entity:
            res_dict['conference_name'] = entity['C'].get('CN')

        #
        # > D. Publisher. The name of the Publisher (e.g. Springer-Nature, Elsevier, ACM, etc.)
        # 'PB',  # Publisher
        res_dict['publisher'] = entity.get("PB")
        #
        # > E. Volume No (if available). This is the journal or series volume number.
        # > It is not available for some preprints or theses.
        # 'V',  # Publication volume
        res_dict['volume'] = entity.get("V")
        #
        # > F. Issue No (if available). This is available only for journals.
        # 'I',  # Publication issue
        res_dict['issue'] = entity.get("I")
        #
        # > G. Pages (if available). For J, B, C, these are the starting-ending pages
        # > within the volume. For electronic publications these might be paper
        # > No and No of pages. For manuscripts, like theses – the total no of pages.
        # 'FP',  # First page of paper in publication
        # 'LP',  # Last page of paper in publication
        res_dict['page_first'] = entity.get("FP")
        res_dict['page_last'] = entity.get("LP")
        #
        # > DOI. This is the DOI of the document.
        # IMPORTANT: The DOI is normalized to uppercase letters, so if querying the field
        # via evaluate/histogram ensure that the DOI value is using all uppercase letters
        # 'DOI',  # Digital Object Identifier
        res_dict['DOI'] = entity.get("DOI")

        #
        # > DOI Link. Is the URL, containing the DOI,
        # > and pointing to the original publication at the Publisher’s resource.
        # 'S',  # List of source URLs of the paper, sorted by relevance ?
        res_dict['urls'] = entity.get("S")

        #
        # > MSF ID. This is the identifier of the doc in the MS Research repository.
        # Id 	Entity ID
        #
        # > Paper Title. This is the title of the document, including the sub-title, if any.
        # 'DN',  # Original paper title
        res_dict['title_raw'] = entity.get("DN")

        return res_dict
    '''

    
    
    
    
    '''
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
    '''

    
    
    
    
    '''
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
    '''



    ''' 
    def saveEntries(self, file, entries):
        thefile = open(file, 'w')
        for entry in entries:
            thefile.write(entry.toCsv())
            thefile.write("\n")
        thefile.close();
'''




'''        
def downloadLevel(dataDir, subscriptionKey, level, files, restEndpoint, verbose=False):

    #outQueueFile = dataDir + "/ms-academic-queue-" + str(level) + ".csv"
    #outNextQueueFile  = dataDir + "/ms-academic-queue-" + str(level + 1) + ".csv"
    #outEntriesFile = dataDir + "/ms-academic-entries-" + str(level) + ".csv"
    #outInvalidFile = dataDir + "/ms-academic-invalid.csv"
    #inExcludeTopicsFile = dataDir + "/in-academic-exclude-topics.txt"
    #inIncludeTopicsFile = dataDir + "/in-academic-include-topics.txt"
    #outQueueSizeFile = dataDir + "/ms-academic-queue-size.txt"

    outQueueFile = files['outQueueFile'].format(str(level))
    outNextQueueFile  = files['outQueueFile'].format( str(level + 1) )
    outEntriesFile = files['outEntriesFile'].format( str(level) )
    outInvalidFile = files['outInvalidFile']
    inExcludeTopicsFile = files['inExcludeTopicsFile']
    inIncludeTopicsFile = files['inIncludeTopicsFile']
    outQueueSizeFile = files['outQueueSizeFile']

    api = Api(subscriptionKey, restEndpoint)

    # load queue in memory
    msAcademicQueue = api.loadList(outQueueFile);
    msAcademicQueueIds = set(msAcademicQueue);

    # load list of indexed entries in memory
    try:
        msAcademicEntries = api.loadEntries(outEntriesFile);
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print(e)
        msAcademicEntries = []

    # load ids of indexed entries in memory
    msAcademicIndexedIds = set([])
    for entry in msAcademicEntries:
        msAcademicIndexedIds.add(entry.entryId)

    # load list of invalid entries in memory
    msAcademicInvalidIds = set(api.loadList(outInvalidFile));

    # load set of invalid topics in memory
    msAcademicExcludeTopicsIds = set(api.loadList(inExcludeTopicsFile));


    msAcademicIncludeTopicsIds = api.loadList(inIncludeTopicsFile)


    counter = 1;
    msAcademicQueueUpdate = set();
    ids = []
    requestCounter = 0

    # print msAcademicQueue

    for id in msAcademicQueue:

        # get list of 80 ids from queue
        ids.append(id);

        if counter % 80 == 0 or len(msAcademicQueue) == counter:

            # load by publication ids
            refs = api.loadByIds(ids, msAcademicIncludeTopicsIds, verbose)
            requestCounter = requestCounter + 1

            allIds = set();
            for tid in ids:
                allIds.add(tid)

            # print allIds

            for en in refs:
                topicIsValid = True
                for t in en.topics:
                    if  t.topicId in msAcademicExcludeTopicsIds:
                        topicIsValid = False;

                contentIsValid = True
                #TODO: test here if text content is similar to set of the seed publications

                if topicIsValid and contentIsValid:
                    en.level = level
                    msAcademicEntries.append(en)
                    msAcademicIndexedIds.add(en.entryId)
                    if en.entryId in allIds:
                        allIds.remove(en.entryId)

                    for newId in en.referencesTo:
                        if (newId not in msAcademicIndexedIds) and (newId not in msAcademicInvalidIds) and (newId not in msAcademicQueueIds):
                            msAcademicQueueUpdate.add(newId)


                print(str(counter) + " of " + str(len(msAcademicQueue)) + " : " + str(en.entryId) + "  " + str(en.entryPublished) + "  ", en.entryTitle.encode('utf-8'))
            
            for tid in allIds:
                msAcademicInvalidIds.add(tid);

            # load by publication rids
            referencedBy = api.loadByRIds(ids, msAcademicIncludeTopicsIds)
            requestCounter = requestCounter + 1
            for entry in referencedBy:
                newId = entry.entryId
                if (newId not in msAcademicIndexedIds) and (newId not in msAcademicInvalidIds) and (newId not in msAcademicQueueIds):
                    msAcademicQueueUpdate.add(newId)


            # save queue size
            queueSize = len(msAcademicQueueUpdate) + len(msAcademicQueue) - counter
            print("NewQueueSize = " + str(queueSize))

            thefile = open(outQueueSizeFile, 'a')
            thefile.write("\n" + str(queueSize))
            thefile.close();

            print(counter, " of ", len(msAcademicQueue), " - OK")
            print("requestCounter = " + str(requestCounter))

            ids = []

        if requestCounter % 50 == 0:
            # save results every 50 calls
            api.saveList(outInvalidFile, msAcademicInvalidIds)
            api.saveEntries(outEntriesFile, msAcademicEntries);
            api.saveList(outNextQueueFile, msAcademicQueueUpdate);
            print("saving intermediate results ...")

        counter = counter + 1

    # save final results
    api.saveList(outInvalidFile, msAcademicInvalidIds)

    api.saveEntries(outEntriesFile, msAcademicEntries);

    api.saveList(outNextQueueFile, msAcademicQueueUpdate);

    print(msAcademicQueueUpdate)


'''



'''


def authorListFromCsv(csvList):
    lst = []
    for csv in csvList:
        if len(csv) > 0:
            lst.append(authorFromCsv(csv))
    return lst


def authorFromCsv(csv):
    au = Author()

    parts = csv.split("@");
    # print parts
    # return
    au.id = parts[0];
    au.name = parts[1];
    if len(parts) > 2:
        au.affiliation = parts[2]
    else:
        au.affiliation = ""

    if len(parts) > 3:
        au.affiliationId = parts[3]
    else:
        au.affiliationId = ""

    return au;


def entryFromCsv(csv):
    if (not isinstance(csv, str) or len(csv) == 0):
        return None

    cols = csv.split("\t")

    en = Entry()
    en.entryId = cols[0]
    en.entryTitle = cols[1]
    en.entryURL = cols[2]
    en.entryPublished = cols[3]
    en.entryAbstract = cols[4]
    en.authors = authorListFromCsv(cols[5].split(";"))
    en.topics = topicListFromCsv(cols[6].split(";"))
    if (len(cols) > 7):
        en.referencesTo = cols[7].split(";")
    else:
        en.referencesTo = []

    if (len(cols) > 8):
        en.referencedBy = cols[8].split(";")
    else:
        en.referencedBy = []

    if (len(cols) > 9):
        en.ECC = int(cols[9])
    else:
        en.ECC = 0

    return en


def topicListFromCsv(csvList):
    lst = []
    for csv in csvList:
        if len(csv) > 0:
            lst.append(topicListFromCsv(csv))
    return lst


def topicListFromCsv(csv):
    to = Topic()
    parts = csv.split("@");
    to.topicId = parts[0]
    to.topicName = parts[1]
    return to



