import json
import math
from nltk.tokenize import word_tokenize

def tf_idf(dataLines):
    result = {}
    for jsonData in dataLines:
        data = json.loads(jsonData)
        if data.get('word') not in result.keys() and data.get('count') != 0:
            idf = count_idf(data)
            tf = count_tf(data)
            tf_idf = {}
            if idf != 0:
                for doc_num in tf.keys():
                    tf_idf[doc_num] = tf.get(doc_num) * idf
            result_for_word = {}
            result_for_word['idf'] = idf
            result_for_word['tf_idf'] = tf_idf
            result[data.get('word')] = result_for_word
            print('INFO: ' + data.get('word') + ' processed')
    return result


def count_tf(data):
    result_for_word = {}
    for doc_num in data.get('inverted_array'):
        with open('./resources/files/' + str(doc_num) + '.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            occurrence_num = 0
            words_num = 0
            for line in lines:
                tokens_list = word_tokenize(line, language="russian")
                occurrence_num += count_words_in_list_by_lemma(tokens_list, data.get('word'))
                words_num += len(tokens_list)
            result_for_word[doc_num] = occurrence_num / words_num
    return result_for_word


def count_words_in_list_by_lemma(list, lemma):
    count = 0
    words_for_lemma = lemmas.get(lemma)
    for token in list:
        if words_for_lemma.__contains__(token):
            count += 1
    return count


def count_idf(data):
    return math.log(100 / data.get('count'))

with open('./result/lemmas.txt', 'r', encoding='utf-8') as lemmas_file:
    lemmas = {}
    lemmmas_lines = lemmas_file.readlines()
    for line in lemmmas_lines:
        words = line.split()
        lemmas[words[0]] = words

with open('./resources/invertedIndex.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    result = tf_idf(lines)

tf_idf_file = open('./result/tf_idf.txt', 'x')
for item in result.items():
    tf_idf_file.write(str(item) + '\n')
