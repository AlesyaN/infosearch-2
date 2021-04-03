import os
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer

# функция токенизации
def tokenize(pages):
    result = []
    stop_words = stopwords.words("russian")
    search = re.compile(r'[^А-Яа-я]').search
    for page in pages:
        words = word_tokenize(page, language="russian")
        for word in words:
            if word not in stop_words and not bool(search(word)):
                result.append(word)
    return result

# функция лемматизации
def lemmatize(tokens):
    result = {}
    morph = MorphAnalyzer()
    for token in tokens:
        lemma = morph.normal_forms(token)[0]
        if not bool(result.get(lemma)):
            result[lemma] = []
        result[lemma].append(token)
    return result


pages = []

# считываем из файлов текст статей
for filename in os.listdir('./resources/files'):
    with open('./resources/files/' + filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            pages.append(line)

# проводим токенизацию и записываем результат в файл
tokens = tokenize(pages)
tokens_file = open('./result/tokens.txt', 'x')
for token in tokens:
    tokens_file.write(token + '\n')

# проводим лемматизацию и записываем результат в файл
lemmas = lemmatize(tokens)
lemmas_file = open('./result/lemmas.txt', 'x')
for key in lemmas:
    lemmas_file.write(key + ' ')
    for value in lemmas[key]:
        lemmas_file.write(value + ' ')
    lemmas_file.write('\n')