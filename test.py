# This python file is to use for tokenize, stemming, and compute word frequency dictionary

from nltk import *
import re




def tokenize(text_content: str) -> [str]:
    check_punctuation = re.compile(r'([^a-zA-Z\s0-9])')
    previous = []
    result = []
    if check_punctuation.search(text_content):
        text_content = check_punctuation.sub(' ', text_content.lower())

    previous = previous + text_content.lower().split()
    while previous:
        word = previous.pop(0)
        if word != '' and len(word) >= 2:
            result.append(word)
    return result


def stemming(tokens_list: list):
    stemmer = PorterStemmer()
    stemmer_list = []

    for w in tokens_list:
        stemmer_list.append(stemmer.stem(w))

    return stemmer_list


def compute_word_frequencies(tokens_list: list) -> {str: int}:
    freq_dict = {}
    for token in tokens_list:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    return freq_dict


# def get_url_path(url: str):
#     parsed = urlparse(url)
#     url_path = parsed.path
#     return url_path