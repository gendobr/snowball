import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import numpy
import random
import jsonlines
from nltk.corpus import stopwords


class CustomTokenizer:
    def __init__(self):
        self.valid_pos_tags = {}
        self.stemmer = False  # PorterStemmer()
        self.tester = False  # re.compile('^[a-zA-Z]+$')
        self.word_dictionary = {}
        self.stop = set([])

    def get_tokens(self, string):
        # print(string)
        text = nltk.word_tokenize(string)
        # print(('text', text))
        tagged_words = nltk.pos_tag(text)
        # print(('tagged_words', tagged_words))
        words = []
        for tw in tagged_words:
            # print(tw)
            if tw[1] in self.valid_pos_tags:
                the_word = tw[0].lower()
                # print(the_word, self.tester.match(the_word))

                if self.tester.match(the_word) and the_word not in self.stop:
                    try:
                        the_word = self.stemmer.stem(tw[0].lower()).encode('utf-8')
                    except IndexError:
                        continue
                    words.append(the_word.decode("utf-8"))
        return words

    def extend_tokens(self, words):
        for tk in words:
            if tk not in self.word_dictionary:
                self.word_dictionary[tk] = len(self.word_dictionary)
        return words

    def exclude_unknown_tokens(self, words):
        return [w for w in words if w in self.word_dictionary]
