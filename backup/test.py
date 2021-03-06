import os
import re
import math

from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict

root_dir = '/Users/mac/Desktop/divided_articles/'
kind_list = os.listdir(root_dir)
link_dir = '/Users/mac/Desktop/article_link.txt'
raw_dir = '/Users/mac/Desktop/articles/'

article_names = []

manual_points = []

def gen_article_list():
    article_list = []
    raw_article_list = []
    for kind in kind_list:
        kind_dir = root_dir + kind + '/'
        file_list = os.listdir(kind_dir)
        for file in file_list:
            f = open(kind_dir + file, encoding='utf-8')
            article = f.read()
            with open(raw_dir + kind + '/' + file, 'r') as ff:
                raw_article = ff.read()
            ff.close
            article_list.append(article)
            raw_article_list.append(raw_article)
            article_names.append(kind + '/' + file)
            f.close
    for i in range(len(article_list)):
        manual_points.append(1.0)
    return article_list, raw_article_list

def get_bag(article_list):
    bag = CountVectorizer(token_pattern='\\b\\w+\\b')
    count = bag.fit_transform(article_list)
    return bag, count

def gen_inverse_index(article_list, bag, array, raw_article_list):
    result = defaultdict(list)
    words = bag.get_feature_names() 
    for index, value in enumerate(article_list):
        for i, word in enumerate(words):
            if array[index][i] != 0:
                position_list = [m.span() for m in re.finditer(r'\b' + word + r'\b', value)]
                result[word].append((index, array[index][i], position_list))
    return result


def get_url_title(name):
    _index = name.index('/')
    
    kind = name[:_index]
    
    file_t = name[_index + 1:]
    _index = file_t.index('.')
    file = file_t[:_index]
    
    file_num = int(file)
    with open(link_dir, 'r') as f:
        s = f.readline()
        s = s[:-1]
        cnt = 0
        while(s != kind and cnt < 124):
            s = f.readline()
            s = s[:-1]
            cnt += 1
        
        for i in range(0, file_num):
            s = f.readline()
            
        url_title = f.readline()
        url_title = url_title[:-1]
        it = re.finditer('http://', url_title)
        lis = [m.span() for m in it]
        url = url_title[lis[0][0]:]
        title = url_title[:lis[0][0]]
        
        # if(len(title) == 1):
        #     print(name)
        if len(title) == 0 or title == ' ':
            title = ''
        elif len(url) == 0 or url == ' ':
            url = ''
        else:
            while(title[len(title) - 1].isspace()):
                title = title[:-1]
    f.close
    return kind, title, url


class resultItem:
    def __init__(self, index, name, text):
        self.index = index
        
        
        kind, title, url = get_url_title(name)
        self.kind = kind
        self.title = title
        self.url = url
        self.text = text
        self.rank = 0
        self.freq = 0
        self.count = 0 # ?????????????????????????????????
        self.occurence = []
        self.similarity = 0.0
        self.manual_point = manual_points[index]
    def __str__(self):
        s = "kind: " + self.kind + \
            "\ntitle: " + self.title + \
            "\nurl: " + self.url + \
            "\nfreq: " + str(self.freq) + \
            "\nrank: " + str(self.rank) + \
            "\npoint: " + str(self.count * self.rank * self.manual_point) + \
            "\nsimilarity: " + str(self.similarity) + \
            "\n"
        for j in self.occurence:
            s += "> ..." + self.text[max(0, j[0] - 30):j[1] + 30] + "...\n"
        return s

def get_similarity(a, b):
    dot = 0
    a_len = 0
    b_len = 0
    for i in range(len(a)):
        dot += a[i] * b[i]
        a_len += a[i] * a[i]
        b_len += b[i] * b[i]
    a_len = math.sqrt(a_len)
    b_len = math.sqrt(b_len)
    return dot / (a_len * b_len)

#inverse_index[word]: [(????????????, ????????????????????????????????????, ???????????????????????????), ...]
def get_result(search_str, inverse_index, article_names, article_list, bag, array):
    word_result = []
    art_set = []
    word_list = search_str.split(' ')
    for word in word_list:
        word_result.append(inverse_index[word])
        for i in inverse_index[word]:
            if i[0] not in art_set:
                art_set.append(i[0])
        
    freq = len(art_set) # ?????????????????????????????????????????????
    
    result_dict = dict()
    for i in word_result: # ???????????????
        if not i:
            continue
        for info in i: # ???????????????????????????????????????
                    # j????????????(????????????, ????????????????????????????????????, ???????????????????????????)
                    # ??????????????????????????????if ????????????else
            if info[0] not in result_dict:
                item = resultItem(info[0], article_names[info[0]], article_list[info[0]])
                
                item.count += 1 # ?????????????????????????????????
                item.freq += info[1] # ?????????????????????????????????
                item.rank += info[1] * 100 / freq # ????????????????????????????????? / ?????????????????????????????????
               
                item.occurence.extend(info[2])
                result_dict[info[0]] = item
            else:
                item = result_dict[info[0]]

                item.count += 1
                item.freq += info[1]
                # print(item.freq)
                item.rank += info[1] * 100 / freq
                
                
                item.occurence.extend(info[2])
                result_dict[info[0]] = item
    result_list = [i for i in result_dict.values()]
    search_vec = CountVectorizer(vocabulary=bag.get_feature_names()).fit_transform([search_str]).toarray()
    for i in result_list:
        i.similarity = get_similarity(search_vec[0], array[i.index].A[0])
    result_list.sort(key=lambda x: -x.rank * x.count * x.manual_point)
    return result_list


if __name__ == '__main__':
    

    article_list, raw_article_list = gen_article_list()
    bag, count = get_bag(article_list)
    
    inverse_index = gen_inverse_index(article_list, bag, count.toarray(), raw_article_list)
    
    while True:
        print('type string you want to search')
        search_str = input()
        if search_str == 'q':
            exit(0)
        result = get_result(search_str, inverse_index, article_names, article_list, bag, count)
        for index, i in enumerate(result):
            print(f'[{index}]:')
            print(i)
        print('choose the best choice above')
        result_num = input()

        art_index = result[int(result_num)].index
        manual_points[art_index] *= 1.1

        
