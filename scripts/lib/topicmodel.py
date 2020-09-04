import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import numpy
import random
import jsonlines
from nltk.corpus import stopwords


#    validPOSTags = {'NNP':True, 'JJ':True, 'NN':True, 'NNS':True, 'JJS':True, 'JJR':True, 'NNPS':True};
#    tester = re.compile('^[a-zA-Z]+$')
#    wordDictionary={}

class io:
    def __init__(self, outputDir):
        self.outputDir = outputDir

    def save_dict_as_csv(self, filename, aDictionary):
        keys = aDictionary.keys()
        fieldnames = ['key', 'value']
        dict_output_file = open(self.outputDir + '/' + filename, 'w')
        writer = csv.DictWriter(dict_output_file, fieldnames=fieldnames, delimiter="\t", quotechar='',
                                quoting=csv.QUOTE_NONE)
        writer.writeheader()

        for k in aDictionary.keys():
            writer.writerow({'key': k, 'value': aDictionary[k]})

        dict_output_file.close()

    def load_csv_as_dict(self, filename):
        csv_input_file = open(self.outputDir + '/' + filename, 'r')
        csvreader = csv.DictReader(csv_input_file, delimiter="\t", quotechar='', quoting=csv.QUOTE_NONE)

        word_dictionary = {}
        word_dictionary_inverse = {}
        for dat in csvreader:
            word_dictionary[dat['key']] = dat['value']
            # wordDictionaryInverse[dat['value']] = dat['key']
        csv_input_file.close()

        return word_dictionary


class Model:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.word_dictionary = {}
        self.word_dictionary_size = 0
        self.word_dictionary_inverse = {}
        self.cooccurrence_probability = []
        self.topic_model = []

    def set_word_dictionary(self, word_dictionary):
        self.word_dictionary_size = len(word_dictionary)
        self.word_dictionary_inverse = {}
        self.word_dictionary = {}
        for key in word_dictionary.keys():
            self.word_dictionary[key] = int(word_dictionary[key])
            self.word_dictionary_inverse[int(word_dictionary[key])] = key
        return

    def coccurences(self, file_path_input, extract_tokens=None):
        norma = 0.0
        random.seed()
        cooccurrence_probability = numpy.zeros((self.word_dictionary_size, self.word_dictionary_size), dtype=numpy.int)
        with jsonlines.open(file_path_input) as reader:
            for item in reader:
                words = extract_tokens(item)
                for i in range(0, len(words)):
                    w1 = words[i]
                    for j in range(i + 1, len(words)):
                        w2 = words[j]
                        if w1 in self.word_dictionary and w2 in self.word_dictionary:
                            w1_pos = int(self.word_dictionary[w1])
                            w2_pos = int(self.word_dictionary[w2])

                            if random.random() < 0.0001:
                                print("update", w1_pos, w2_pos)
                            cooccurrence_probability[w1_pos][w2_pos] = cooccurrence_probability[w1_pos][w2_pos] + 1
                            cooccurrence_probability[w2_pos][w1_pos] = cooccurrence_probability[w1_pos][w2_pos]
                            norma += 2
                        # else:
                        #    print "invalid pair ", w1, w2
        print("Counting finished")
        # =============================================
        norma = 1.0 / norma
        print(('norma', norma))
        return cooccurrence_probability * norma

    def word_probability(self, cooccurrence_probability):

        word_probability = numpy.zeros(self.word_dictionary_size)

        for i in range(0, self.word_dictionary_size):
            for j in range(0, self.word_dictionary_size):
                word_probability[i] = cooccurrence_probability[i][j] + word_probability[i]
        # print word_probability
        return word_probability

    def stopwords(self, cooccurrence_probability, h_max):
        word_probability = self.word_probability(cooccurrence_probability)

        entropy = numpy.zeros(self.word_dictionary_size)
        for i in range(0, self.word_dictionary_size):
            if word_probability[i] > 0:
                z = 1.0 / word_probability[i]
                for j in range(0, self.word_dictionary_size):
                    if cooccurrence_probability[i][j] > 0:
                        term = cooccurrence_probability[i][j] * z
                        entropy[i] -= term * numpy.log(term)

        # get maximal allowed entropy value
        sorted_entropy = numpy.sort(entropy)
        sorted_entropy = sorted_entropy[::-1]
        print(("sortedEntropy", sorted_entropy.tolist()))

        number_of_words = len(sorted_entropy)
        entropy_max_value_pos = int(number_of_words * h_max) - 1
        if entropy_max_value_pos < 0:
            entropy_max_value_pos = 0
        print("entropyMaxValuePos=", entropy_max_value_pos)
        entropy_max_value = sorted_entropy[entropy_max_value_pos]

        print("entropyMaxValue=", entropy_max_value)

        # stop-words are ones having large entropy
        stopwords = {}
        for i in range(0, self.word_dictionary_size):
            if entropy[i] > entropy_max_value:
                # stopwords[i] = self.wordDictionaryInverse[i]
                stopwords[self.word_dictionary_inverse[i]] = i
                print((i, self.word_dictionary_inverse[i], entropy[i]))
                # print i, entropy[i]
        return stopwords

    def rare_words(self, cooccurrence_probability, alpha):

        word_probability = self.word_probability(cooccurrence_probability)

        # get maximal allowed entropy value
        sorted_word_probability = numpy.sort(word_probability)
        # print sorted_word_probability.tolist()

        summa = 0
        i = -1
        while summa <= alpha:
            i = i + 1
            summa = summa + sorted_word_probability[i]
        probability_min_value = sorted_word_probability[i]
        print(("probabilityMinValue=", probability_min_value))

        # stop-words are ones having large entropy
        rare_words = {}
        i_max = len(sorted_word_probability) - 1
        for i in range(0, i_max):
            if word_probability[i] <= probability_min_value:
                # rare_words[i] = word_dictionary_inverse[i]
                rare_words[self.word_dictionary_inverse[i]] = i
                print((i, self.word_dictionary_inverse[i], word_probability[i]))

        return rare_words

    def rare_words_memory_optimal(self, file_path_input, alpha, extract_tokens=None):

        # =====================================================
        # count words
        word_probability = numpy.zeros(self.word_dictionary_size)
        random.seed()
        norma = 0
        with jsonlines.open(file_path_input) as reader:
            for item in reader:
                for w1 in extract_tokens(item):
                    if w1 in self.word_dictionary:
                        w1position = int(self.word_dictionary[w1])
                        word_probability[w1position] += 1
                        norma += 1

        norma = 1.0 / norma
        word_probability = word_probability * norma
        print(('norma', norma))
        print("Counting finished")
        # /count words
        # =====================================================

        # =====================================================
        # get minimal allowed probability value
        sorted_word_probability = numpy.sort(word_probability)
        summa = 0
        i = -1
        while summa <= alpha:
            i = i + 1
            summa = summa + sorted_word_probability[i]
        probability_min_value = sorted_word_probability[i]
        print(("probability_min_value=", probability_min_value))
        # /get minimal allowed probability value
        # =====================================================

        rare_words = {}
        i_max = len(sorted_word_probability) - 1
        for i in range(0, i_max):
            if word_probability[i] <= probability_min_value:
                rare_words[self.word_dictionary_inverse[i]] = i
                # print((i, self.word_dictionary_inverse[i], word_probability[i]))

        return rare_words

    def reduced_dictionary(self, word_dictionary, stopwords, rare_words):
        reduced_word_dictionary = {}
        iw = 0
        for word in word_dictionary.keys():
            if not (word in stopwords or word in rare_words):
                reduced_word_dictionary[word] = iw
                iw = iw + 1

        return reduced_word_dictionary

    def model_from_factor(self, H):

        n_words = len(H)
        n_topics = len(H[0])

        N = numpy.zeros(n_topics)
        P = numpy.zeros((n_words, n_topics))

        for iTopic in range(0, n_topics):

            # c1 = H.T[iTopic]

            norm = 0
            for p in H.T[iTopic]:
                norm = norm + p

            print(("topic", str(iTopic), "probability", norm * norm))

            if norm > 0:
                for i in range(0, n_words):
                    P.T[iTopic][i] = H.T[iTopic][i] / norm

            N[iTopic] = norm * norm

        return {'P': P, 'N': N}

    def load_topic_model(self, cooccurrence_probability, topic_model):

        # covariance
        self.cooccurrence_probability = cooccurrence_probability

        # topic model
        self.topic_model = topic_model

        # topic probability
        self.pt = topic_model['N']

        # word probability
        self.pw = numpy.zeros(self.word_dictionary_size)
        for i in range(0, len(self.cooccurrence_probability)):
            s = 0
            for j in range(0, len(self.cooccurrence_probability)):
                s = s + self.cooccurrence_probability[i][j]
            self.pw[i] = s
        print(self.pw)
        # return

        self.pwt = topic_model['P']
        self.n_words = len(self.pwt)
        self.n_topics = len(self.pwt[0])
        print(("n_words", self.n_words, " n_topics", self.n_topics))
        # return

        self.ptw = numpy.zeros((self.n_topics, self.n_words))  # numpy.save('out/TopicModel.npy', {'H':H, 'N':N})

        for iWord in range(0, self.n_words):
            for iTopic in range(0, self.n_topics):
                if self.pw[iWord] > 0:
                    self.ptw[iTopic][iWord] = self.pwt[iWord][iTopic] * self.pt[iTopic] / self.pw[iWord]

    def topics_from_doc(self, words):

        pwd = numpy.zeros(self.n_words)
        word_total = len(words)

        for word in words:
            # print word
            if word in self.word_dictionary:
                # print word, self.wordDictionary[word]
                i_word = self.word_dictionary[word]
                if i_word < self.n_words:
                    pwd[i_word] = pwd[i_word] + 1
                else:
                    print(("word, iWord = ", word, i_word))
        # return
        # print wordTotal, pwd.tolist()
        # return

        norm = 1.0 / max(word_total, 1)
        for i in range(0, self.n_words):
            pwd[i] = pwd[i] * norm

        # print wordTotal, pwd.tolist()
        # return

        ptd = numpy.zeros(self.n_topics)
        for iTopic in range(0, self.n_topics):
            s = 0
            for i_word in range(0, self.n_words):
                s = s + self.ptw[iTopic][i_word] * pwd[i_word]
            # print ptw[iTopic].tolist()
            # print pwd.tolist()
            # print "iTopic=", iTopic, " s=",s
            # print "=================="

            ptd[iTopic] = s

        return ptd

