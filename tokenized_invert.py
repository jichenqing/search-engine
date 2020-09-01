# This part is the index creating part
# This file create the index files for the retrieval part
# It use pickle to save the index files
import json
from bs4 import BeautifulSoup
import os
import test
from collections import defaultdict
import pickle
import re

url_list = []
doc_content = dict()
inverse_index = defaultdict(list)

files = ["Indexing/www-db_ics_uci_edu", "Indexing/www_cs_uci_edu", "Indexing/www_informatics_uci_edu"]


def main_func(file_name):
    for file in os.listdir(file_name):
        with open(os.path.join(file_name,file)) as f:
            data = json.load(f)
            if data['url'].find('?ical=1') == -1: #and data['url'] == 'https://www.cs.uci.edu/events-page/computer-science-seminar-series/':
                soup_page = BeautifulSoup(data['content'], 'lxml')

                for tag in soup_page.find_all('a'): # delete anchor text part
                    tag.replaceWith('')

                if soup_page.find('title'):
                    title_text_list = test.stemming(test.tokenize(soup_page.find('title').get_text()))

                bold_text_elements = [t for t in soup_page.find_all(text=True) if t.parent.name == 'b']

                strong_text_elements = [t for t in soup_page.find_all(text=True) if t.parent.name == 'strong']

                bold_text_list = [] # find bold text
                for i in bold_text_elements:
                    bold_text_list += test.stemming(test.tokenize(i))

                strong_text_list = [] # find strong text
                for j in strong_text_elements:
                    strong_text_list += test.stemming(test.tokenize(j))

                heading_dict = {} # find heading text
                for heading in soup_page.find_all([f'h{i}' for i in range(1, 4)]):
                    heading_stem = test.stemming(test.tokenize(heading.text.strip()))
                    if heading_stem:
                        for h in heading_stem:
                            if h not in heading_dict:
                                heading_dict[h] = heading.name

                text = soup_page.get_text()

                #print(text)
                #break
                url_address = data['url']
                url_address = re.sub(r'#.*', '', url_address) # delete fragment part

                if url_address in url_list: # avoid duplicate fragment part
                    pass
                else:
                    url_list.append(url_address)
                    tokens_list = test.tokenize(text)
                    stemming_list = test.stemming(tokens_list)
                    frequency_dict = test.compute_word_frequencies(stemming_list)

                    for key in frequency_dict:

                        position_list = [i for i in range(len(stemming_list)) if stemming_list[i] == key]

                        if key in title_text_list:
                            inverse_index[key].append(((url_list.index(url_address)+1), frequency_dict[key], 'title', position_list))
                        elif key in heading_dict:
                            inverse_index[key].append(((url_list.index(url_address) + 1), frequency_dict[key], heading_dict[key], position_list))
                        elif key in bold_text_list:
                            inverse_index[key].append(((url_list.index(url_address) + 1), frequency_dict[key], 'bold', position_list))
                        elif key in strong_text_list:
                            inverse_index[key].append(((url_list.index(url_address) + 1), frequency_dict[key], 'strong', position_list))
                        else:
                            inverse_index[key].append(((url_list.index(url_address) + 1), frequency_dict[key], '', position_list))

                    doc_content[url_list.index(url_address)+1] = frequency_dict
                    #inverse_index[key].append((url_address, frequency_dict[key]))

# key_list = sorted(inverse_index)
# for i in key_list:
#     print(i)

# def boolean_retrieval(query):
#     query_list = test.tokenize(query)
#     query_stemming = test.stemming(query_list)
#
#     result = set()
#     for term in query_stemming:
#         if term in inverse_index:
#             doc_set = set([i[0] for i in inverse_index[term]])
#             if result == set():
#                 result = doc_set
#             else:
#                 result = doc_set.intersection(result)
#
#     word_freq_dict = defaultdict(list)
#     for word in query_stemming:
#             for doc_id, freq in inverse_index[word].items():
#                 pass


# *****************
# Main area to function
for i in files:
    main_func(i)

# for k in inverse_index:
#     inverse_index[k] = sorted(inverse_index[k], key=lambda x: -x[1])
#
# *****************
# Save invert_index, url_list as pickle, load in boolean_retrieval
#pickle.dump(inverse_index, open("inverse_index.p", "wb"))
# pickle.dump(url_list, open("url_list.p", "wb"))
#pickle.dump(content_length, open("content_length.p", "wb"))
#pickle.dump(doc_content, open("doc_content.p", "wb"))
#print(inverse_index)
print('done')
# print(boolean_retrieval('ACM'))


# with open('index_table_no_repeat.txt', 'w') as fh:
#     fh.write("unique number of tokens: " + str(len(inverse_index)) + "\n")
#     fh.write("total number of pages: " + str(len(url_list)) + "\n")
#
#     for k in inverse_index:
#         inverse_index[k] = sorted(inverse_index[k], key=lambda x: -x[1])
#     #for k in sorted(inverse_index, key=lambda x: x[-1]):
#     #for k, v in inverse_index.items():
#         fh.write(k + ' -> ')
#
#         if len(inverse_index[k]) == 1:
#             fh.write(str(inverse_index[k][0][0]) + " : " + str(inverse_index[k][0][1]))
#         else:
#             for j in inverse_index[k][:-1]:
#                 fh.write(str(j[0]) + " : " + str(j[1]) + " , ")
#             fh.write(str(inverse_index[k][-1][0]) + " : " + str(inverse_index[k][-1][1]))
#
#         fh.write("\n")


# with open('tokens11.txt', 'w') as fi:
#     for k in inverse_index:
#         fi.write(k + '\n')


# for file in os.listdir("Indexing/www_cs_uci_edu"):
#     with open(os.path.join("Indexing/www_cs_uci_edu",file)) as f:
#         data = json.load(f)
#         soup_page = BeautifulSoup(data['content'], 'lxml')
#         text = soup_page.get_text()
#         if re.compile(r'([^a-zA-Z\s0-9])').search(text):
#             text = re.compile(r'([^a-zA-Z\s0-9])').sub(' ', text.lower())
#         previous = previous + text.lower().split()
#         while previous:
#             word = previous.pop(0)
#             if word != '' and len(word) >= 2:
#                 result.append(word)
#
#         print(result)



# with open("Indexing/www-db_ics_uci_edu/2b8cbd2476f476856e9b95539c6b9b9f3e34841863c922f15dce4bbebb3ed245.json") as f:
#     data = json.load(f)
#     print(data['url'])
#
#
#
#     soup_page = BeautifulSoup(data['content'], 'lxml')


    # text=soup_page.stripped_strings
    # for string in text:
    #     print(string)
    #print(soup_page.get_text())

    #bold_text_elements = [t for t in soup_page.find_all(text=True) if t.parent.name == 'b']

    #paragraph_text_elements = [t for t in soup_page.find_all(text=True) if t.parent.name == 'p']
    #print('bold', bold_text_elements)
    #print(soup_page.get_text())
    #print(soup_page.find_all('b'))


    #if soup.find_all('a') is not None:
        #if len(soup.find_all('a')) >= 1:
            #for link in soup.find_all('a'):
                #if link.get('href') is not None:
                    #if len(link.get('href')) >= 1:
                        #link = link.get('href').split('#')[0]
                        #print(link)