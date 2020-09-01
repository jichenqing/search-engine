# This is the main information retrieval part
# Include ranking use cosine similarity, field score, and position proximity serach
# The results are ranks by the scores
import pickle
import test
from collections import defaultdict
import math
from datetime import datetime
import numpy as np

inverse_index = pickle.load(open('inverse_index.p', 'rb'))
url_list = pickle.load(open('url_list.p', 'rb'))
#stop_words = [line.rstrip('\n') for line in open("stop_words.txt")]
doc_content = pickle.load(open('doc_content.p', 'rb'))  # {doc_id : {term : freq}}


def substract_lists(a, b):
    count = 0
    for i in a:
        for j in b:
            if abs(i-j) == 1:
                count += 1
    return count


# Calculate abs value of position
def cal_position(position_dict, query_length):
    position_dict_new = defaultdict(int)
    for i in position_dict:
        position_list = position_dict[i]
        if len(position_list) < query_length:
            position_dict[i] = 0
        else:
            position_list = sorted(position_list, key=lambda x: len(x))
            for j in range(query_length-1):
                position_dict_new[i] += substract_lists(position_list[j], position_list[j+1])

            #position_list = tuple(position_list)
            #position_dict_new[i] = substract_lists(*position_list)

    return position_dict_new


# Calculate cos similarity of two vectors
def cosine(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    return np.dot(v1, v2) / (np.sqrt(np.sum(v1**2)) * np.sqrt(np.sum(v2**2)))


# Calculate term frequency
def tf(freq):
    #if term in inverse_index:
        #return float(1 + math.log((freq / length), 10)) # have negative value?
    return float(1 + math.log(freq, 10))
    # else:
    #     return 0


# Calculate idf
def idf(term):
    if term in inverse_index:
        if len(inverse_index[term]) != 0:
            return float(math.log((len(url_list) / len(inverse_index[term])), 10))
        else:
            return 0


def boolean_retrieval(query):
    query_list = test.tokenize(query)
    query_stemming = test.stemming(query_list)
    query_dict = test.compute_word_frequencies(query_stemming)  # query frequency dict
    query_length = len(query_dict)

    result = set()  # first find doc contain all terms

    for term in query_dict:
        if term in inverse_index:
            doc_set = set([i[0] for i in inverse_index[term]])
            if result == set():
                result = doc_set
            else:
                result = doc_set.union(result)

        #term_tf.append(tf(term, query_dict[term]))
        #term_idf.append(idf(term))

    word_freq_dict = defaultdict(list) #{doc_id: [(term1, freq1), (term2, freq2)]}

    final_dict = {}

    field_dict = defaultdict(int)  # {docid: sum of field sccore}
    field_score = {'title': float(math.log(10, 10)), 'h1': float(math.log(5, 10)), 'h2': float(math.log(4, 10)), 'h3': float(math.log(3, 10)), 'bold': float(math.log(2, 10)), 'strong': float(math.log(2, 10))}

    position_dict = defaultdict(list) # doc_id : [[1,2],[3,4],...]


    for word in query_dict:
        #if word not in stop_words:
        for doc_id, freq, field, position_list in inverse_index[word]:
            if doc_id in result:
                word_freq_dict[doc_id].append((word, freq))

                if query_length >= 2:
                    position_dict[doc_id].append(position_list)

                if field != '':
                    field_dict[doc_id] += field_score[field]

    #for j in range(query_length-1):

    for document, freq_list in word_freq_dict.items():
        final_dict[document] = sum([i[1] for i in freq_list])  # {doc_id: sum of all term freq of a doc}

    sort_dict = {k: v for k, v in sorted(final_dict.items(), key=lambda item: -item[1])}  # sort by frequency

    cos_dict = dict()  # cosine similarity use lnc.ltc

    position_dict = cal_position(position_dict, query_length)
    #print(position_dict)

    for i in sort_dict:
        query_vector = []
        document_vector = []
        total_set = set(query_stemming).union(set(list(doc_content[i].keys())))
        for term in total_set:
            if term in inverse_index:
                if term in query_dict:
                    query_vector.append(tf(query_dict[term]) * idf(term))  # calculate tf and idf for query
                else:
                    query_vector.append(0)

            if term in doc_content[i]:
                document_vector.append(tf(doc_content[i][term]))  # calculate tf for document
            else:
                document_vector.append(0)

        cos = cosine(query_vector, document_vector)  # calculate cosine similarity betwen query and document

        cos_dict[i] = cos + field_dict[i] # {doc_id : cosine similarity + field score}
        if i in position_dict:
            if position_dict[i] != 0:
                cos_dict[i] += float(math.log(2,10)) * math.log(position_dict[i],10)


    # for doc, tf_idf in word_tf_idf.items():
    #     word_tf_idf[doc] = cosine([term_tf[i] * term_idf[i] for i in range(len(term_tf))], tf_idf)

    # print(word_freq_dict)
    # print('termtf', term_tf)
    # print('termidf', term_idf)
    #print('term tf*idf', [term_tf[i] * term_idf[i] for i in range(len(term_tf))]) #tf-idf for query

    #print(cosine(term_tf, term_idf))

    # sort_d = {k: v for k, v in sorted(word_tf_idf.items(), key=lambda item: -item[1])}
    # print(sort_d)
    # k = 0
    # for i in list(sort_d.keys())[:5]:
    #     print(str(k) + '.' + ' ' + url_list[i - 1])
    #     k += 1

    #return {k: v for k, v in sorted(final_dict.items(), key=lambda item: -item[1])}

    return {k: v for k, v in sorted(cos_dict.items(), key=lambda item: -item[1])}  # sort by decreasing cosine similarity


def show_result(term: str):
    final_string = '\n    ******** ' + 'results for: ' + term  + ' ********  ' + '\n'*2

    final_url_list = []
    url_list_string_list = []

    start = datetime.now()
    final = boolean_retrieval(term)
    #print(final)

    k = 1
    if final:
        for i in list(final.keys()):#[:10]:
            url_list_string_list.append(str(k) + '.' + ' ' + url_list[i - 1])
            final_url_list.append(url_list[i - 1])
            k += 1
    else:
        final_string += ' Sorry, We cannot find result for this query'
    time = 'Search takes: ' + str(datetime.now() - start)

    #print(final_string)
    #print(time)
    return final_string, time, url_list_string_list, final_url_list


#show_result('receive acm award')
# print(final)
# k = 1
# for i in list(final.keys())[:5]:
#     print(str(k) + '.' + ' ' + url_list[i-1])
#     k += 1
