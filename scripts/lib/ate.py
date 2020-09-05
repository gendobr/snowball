# import PyPDF2
import nltk
from nltk.tag.perceptron import PerceptronTagger
import numpy as np
import pandas as pd
import re
import ahocorasick


# noun adj prep + ? ( ) * |
class POSSequenceDetector:
    def __init__(self, _pattern):
        self.pattern = str(_pattern).lower()
        # self.lemmatizer = WordNetLemmatizer()
        self.rule = re.compile(r'\W')
        tokens = []
        i = 0
        ptlen = len(self.pattern)
        while i < ptlen:
            # print i, self.pattern[i:]
            if self.pattern[i:].startswith(' '):
                i = i + 1
            elif self.pattern[i:].startswith('noun'):
                tokens.append('N')  # noun
                i = i + 4
            elif self.pattern[i:].startswith('prep'):
                tokens.append('P')  # preposition
                i = i + 4
            elif self.pattern[i:].startswith('adj'):
                tokens.append('A')  #
                i = i + 3
            elif self.pattern[i:].startswith('+'):
                tokens.append('+')
                i = i + 1
            elif self.pattern[i:].startswith('?'):
                tokens.append('?')
                i = i + 1
            elif self.pattern[i:].startswith('|'):
                tokens.append('|')
                i = i + 1
            elif self.pattern[i:].startswith('*'):
                tokens.append('*')
                i = i + 1
            elif self.pattern[i:].startswith('('):
                tokens.append('(')
                i = i + 1
            elif self.pattern[i:].startswith(')'):
                tokens.append(')')
                i = i + 1
            elif self.pattern[i:].startswith('['):
                tokens.append('[')
                i = i + 1
            elif self.pattern[i:].startswith(']'):
                tokens.append(']')
                i = i + 1
            else:
                raise ValueError('Unknown symbol in pattern ' + self.pattern + ' at position ' + i)
        # print(tokens)
        self.pattern = ''.join(tokens)
        # print self.pattern
        self.prog = re.compile(self.pattern)

        self.map = {
            '$': '-',  # dollar / $ -$ --$ A$ C$ HK$ M$ NZ$ S$ U.S.$ US$
            "''": '-',  # closing quotation mark / ' ''
            '(': '-',  # opening parenthesis / ( [ {
            ')': '-',  # closing parenthesis / ) ] }
            ',': '-',  # comma / ,
            '--': '-',  # dash / --
            '.': '-',  # sentence terminator / . ! ?
            ':': '-',  # colon or ellipsis / : ; ...
            '``': '-',  # ': opening quotation mark    ` `
            'CD': '9',
            # numeral, cardinal / mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025 fifteen 271,124 dozen quintillion DM2,000 ...
            'JJ': 'A',
            # adjective or numeral, ordinal / third ill-mannered pre-war regrettable oiled calamitous first separable ectoplasmic battery-powered participatory fourth still-to-be-named multilingual multi-disciplinary ...
            'JJR': 'A',
            # adjective, comparative / bleaker braver breezier briefer brighter brisker broader bumper busier calmer cheaper choosier cleaner clearer closer colder commoner costlier cozier creamier crunchier cuter ...
            'JJS': 'A',
            # adjective, superlative / calmest cheapest choicest classiest cleanest clearest closest commonest corniest costliest crassest creepiest crudest cutest darkest deadliest dearest deepest densest dinkiest ...
            'RB': 'B',
            # adverb / occasionally unabatingly maddeningly adventurously professedly stirringly prominently technologically magisterially predominately swiftly fiscally pitilessly ...
            'RBR': 'B',
            # adverb, comparative / further gloomier grander graver greater grimmer harder harsher healthier heavier higher however larger later leaner lengthier less-perfectly lesser lonelier longer louder lower more ...
            'RBS': 'B',
            # adverb, superlative / best biggest bluntest earliest farthest first furthest hardest heartiest highest largest least less most nearest second tightest worst
            'CC': 'C',
            # conjunction, coordinating / & 'n and both but either et for less minus neither nor or plus so therefore times v. versus vs. whether yet
            'DT': 'D',
            # determiner / all an another any both del each either every half la many much nary neither no some such that the them these this those
            'EX': 'E',  # existential there / there
            'FW': 'F',
            # foreign word / gemeinschaft hund ich jeux habeas Haementeria Herr K'ang-si vous lutihaw alai je jour objets salutaris fille quibusdam pas trop Monte terram fiche oui corporis ...
            'POS': 'G',  # genitive marker / ' 's
            'RP': 'I',
            # particle / aboard about across along apart around aside at away back before behind by crop down ever fast for forth from go high i.e. in into just later low more off on open out over per pie raising start teeth that through under unto up up-pp upon whole with you
            'LS': '-',
            # list item marker / A A. B B. C C. D E F First G H I J K One SP-44001 SP-44002 SP-44005 SP-44007 Second Third Three Two * a b c d first five four one six three two
            'MD': 'M',
            # modal auxiliary / can cannot could couldn't dare may might must need ought shall should shouldn't will would
            'NN': 'N',
            # noun, common, singular or mass / common-carrier cabbage knuckle-duster Casino afghan shed thermostat investment slide humour falloff slick wind hyena override subhumanity machinist ...
            'NNP': 'N',
            # noun, proper, singular / Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA Shannon A.K.C. Meltex Liverpool ...
            'NNPS': 'N',
            # noun, proper, plural / Americans Americas Amharas Amityvilles Amusements Anarcho-Syndicalists Andalusians Andes Andruses Angels Animals Anthony Antilles Antiques Apache Apaches Apocrypha ...
            'NNS': 'N',
            # noun, common, plural / undergraduates scotches bric-a-brac products bodyguards facets coasts divestitures storehouses designs clubs fragrances averages subjectivists apprehensions muses factory-jobs ...
            'TO': 'O',  # "to" as preposition or infinitive marker / to
            'IN': 'P',
            # preposition or conjunction, subordinating / astride among uppon whether out inside pro despite on by throughout below within for towards near behind atop around if like until below next into if beside ...
            'PRP': 'R',
            # pronoun, personal / hers herself him himself hisself it itself me myself one oneself ours ourselves ownself self she thee theirs them themselves they thou thy us
            'PRP$': 'R',  # pronoun, possessive / her his mine my our ours their thy your
            'PDT': 'T',  # pre-determiner / all both half many quite such sure this
            'UH': 'U',
            # interjection / Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly man baby diddle hush sonuvabitch ...
            'VB': 'V',
            # verb, base form / ask assemble assess assign assume atone attention avoid bake balkanize bank begin behold believe bend benefit bevel beware bless boil bomb boost brace break bring broil brush build ...
            'VBD': 'V',
            # verb, past tense / dipped pleaded swiped regummed soaked tidied convened halted registered cushioned exacted snubbed strode aimed adopted belied figgered speculated wore appreciated contemplated ...
            'VBG': 'V',
            # verb, present participle or gerund / telegraphing stirring focusing angering judging stalling lactating hankerin' alleging veering capping approaching traveling besieging encrypting interrupting erasing wincing ...
            'VBN': 'V',
            # verb, past participle /  multihulled dilapidated aerosolized chaired languished panelized used experimented flourished imitated reunifed factored condensed sheared unsettled primed dubbed desired ...
            'VBP': 'V',
            # verb, present tense, not 3rd person singular / predominate wrap resort sue twist spill cure lengthen brush terminate appear tend stray glisten obtain comprise detest tease attract emphasize mold postpone sever return wag ...
            'VBZ': 'V',
            # verb, present tense, 3rd person singular / bases reconstructs marks mixes displeases seals carps weaves snatches slumps stretches authorizes smolders pictures emerges stockpiles seduces fizzes uses bolsters slaps speaks pleads ...
            'WDT': 'W',  # WH-determiner / that what whatever which whichever
            'WP': 'W',  # WH-pronoun / that what whatever whatsoever which who whom whosoever
            'WP$': 'W',  # WH-pronoun, possessive / whose
            'WRB': 'W',  # Wh-adverb / how however whence whenever where whereby whereever wherein whereof why
            'SYM': '-'  # symbol / % & ' '' ''. ) ). * + ,. < = > @ A[fj] U.S U.S.S.R * ** ***
        }

    def encode(self, symbol):
        return self.map[symbol] if symbol in self.map else '?'

    def detect(self, pos_tagged_sequence):
        terms = []
        pos_tagged_sequence_encoded = ''.join([self.encode(m[1]) for m in pos_tagged_sequence])
        # print pos_tagged_sequence_encoded
        pos = 0
        m = self.prog.search(pos_tagged_sequence_encoded, pos)
        while m:
            seq = [self.rule.sub('', t[0].lower()) for t in pos_tagged_sequence[m.start():m.end()]]

            last_index = len(seq) - 1
            # seq[last_index]=self.lemmatizer.lemmatize(seq[last_index])
            terms.append(seq)
            pos = m.end()
            m = self.prog.search(pos_tagged_sequence_encoded, pos)
        return terms


class StopWordsDetector:
    def __init__(self, _stopwords):
        self.stopwords = set(_stopwords)
        # print self.stopwords

    def detect(self, lst):
        if isinstance(lst, str):
            if lst in self.stopwords:
                return [lst]
            else:
                return []
        try:
            return [e for e in lst if e in self.stopwords]
        except TypeError:
            s = str(lst)
            print(s in self.stopwords)
            if s in self.stopwords:
                return [s]
            else:
                return []


# fp = open(doc_file, "r")
# doc_txt = fp.read()
# fp.close()
# doc_txt = unicode(doc_txt, "utf-8", errors='ignore')
# doc_txt = re.sub(r'et +al\.', 'et al', doc_txt)
# doc_txt = re.split(r'[\r\n]', doc_txt)
#
#
# term_extractor = ate.TermExtractor(stopwords=stopwords, term_patterns=term_patterns, min_term_words=min_term_words, min_term_length=min_term_length)
# terms = term_extractor.extract_terms(doc_txt)
# c_values = term_extractor.c_values(terms, trace=True)


class TermExtractor:
    def __init__(self, stopwords=[], term_patterns=[], min_term_length=3, min_term_words=2):
        # StopWordsDetector
        self.stopwords = set(stopwords)
        self.min_term_length = min_term_length
        self.term_patterns = term_patterns
        self.min_term_words = min_term_words
        self.detectors = []
        self.pos_tagger = PerceptronTagger()
        for tp in term_patterns:
            self.detectors.append(POSSequenceDetector(tp))

        self.swd = StopWordsDetector(self.stopwords)

    def extract_terms(self, doc_txt, trace=False):
        sent_tokenize_list = filter(lambda x: len(x) > 0, map(lambda s: nltk.tokenize.sent_tokenize(s), doc_txt))
        sentences = []
        _ = [sentences.extend(lst) for lst in sent_tokenize_list]
        if trace:
            print('len(sentences)=' + str(len(sentences)))

        terms = []  # pd.DataFrame(columns=['term'])
        # sentences = sentences[:30]

        i = 1
        filter_fn = lambda x: len(x) >= self.min_term_length
        max_i = len(sentences)
        for s in sentences:
            text = nltk.word_tokenize(s)
            # sent_pos_tags=nltk.pos_tag(text, tagset='universal')
            sent_pos_tags = self.pos_tagger.tag(text)
            sentence_terms = set()
            for fsa1 in self.detectors:
                stn = filter(filter_fn, [' '.join(t) for t in fsa1.detect(sent_pos_tags) if
                                         len(t) >= self.min_term_words and len(self.swd.detect(t)) == 0])
                sentence_terms.update(stn)
            terms.extend([str(trm).strip() for trm in sentence_terms])
            if trace:
                print(i, '/', max_i, s)
            i = i + 1
        return terms

    '''

    '''

    def c_values(self, terms, trace=False):
        terms_df = pd.DataFrame(terms, columns=['term'])
        terms_df['w'] = 1
        terms_df['len'] = len(terms_df['term'])
        term_stats = terms_df.groupby(['term'])['w'].agg([np.sum])
        term_stats['len'] = list(pd.Series(term_stats.index).apply(lambda x: len(x)))

        term_series = list(term_stats.index)
        n_terms = len(term_series)

        for i in range(0, n_terms):
            term_series[i] = ' ' + str(term_series[i]) + ' '

        term_stats['trm'] = term_series
        term_stats.set_index('trm', inplace=True)

        A = ahocorasick.Automaton()
        for i in range(0, n_terms):
            A.add_word(term_series[i], (i, term_series[i]))
        A.make_automaton()

        is_part_of = []
        for i in range(0, n_terms):
            haystack = term_series[i]
            for end_index, (insert_order, original_value) in A.iter(haystack):
                if original_value != haystack:
                    # print original_value, "insideof ", haystack
                    is_part_of.append((original_value, haystack, 1))
        subterms = pd.DataFrame(is_part_of, columns=['term', 'part_of', 'w']).set_index(['term', 'part_of'])

        if trace:
            print("terms/subterms relations discovered ...")

        c_values = []
        # term_series=['time']
        for t in term_series:
            if t in term_stats.index:
                current_term = term_stats.loc[t]
                # average frequency of the superterms
                c_value = 0
                if t in subterms.index:
                    subterm_of = list(subterms.loc[t].index)
                    for st in subterm_of:
                        c_value -= term_stats.loc[st]['sum']
                    c_value /= float(len(subterm_of))

                # add current term frequency
                c_value += current_term['sum']

                # multiply to log(term length)
                c_value = c_value * np.log(current_term['len']) if current_term['len'] > 0 else 0
                if trace:
                    print(t, 'freq=', current_term['sum'], ' cvalue=', c_value)
                c_values.append(c_value)
                # break

        return sorted(zip([x.strip() for x in term_series], c_values), key=lambda x: x[1], reverse=True)
    # sentences[0:10]
    # print self.stopwords

