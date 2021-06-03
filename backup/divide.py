import os
import jieba
import jieba.posseg as psg

def mySave(savepath, content):
    with open(savepath, "wb") as fp:
        fp.write(content)

def myRead(path):
    with open(path, "rb") as fp:
        content = fp.read()
    return content

stop_words = []
def init_stop_words():
    with open('/Users/mac/Desktop/stop_words.txt', 'r') as f:
        content = f.readlines()
        for line in content:
            stop_words.append(line[:-1])
            
def myparse(raw_path, parse_path):
    kindlist = os.listdir(raw_path)
    for mydir in kindlist:
        this_path = raw_path + mydir + '/'
        parse_dir = parse_path + mydir + '/'
        if not os.path.exists(parse_dir):
            os.mkdir(parse_dir)
        file_list = os.listdir(this_path)


        for file_path in file_list:
            fullname = this_path + file_path
            content = myRead(fullname)
            content = content.replace('\r\n'.encode('utf-8'), ''.encode('utf-8')).strip()
            content = content.replace(' '.encode('utf-8'), ''.encode('utf-8')).strip()
            # content_seg = jieba.cut(content)
            content_seg = psg.cut(content)
            n_list = []
            for x in content_seg:
                if 'n' in x.flag:
                    n_list.append(x.word)
            # print(content_fenci)
            ccontent_seg = []
            for word in n_list:
                if word not in stop_words:
                    ccontent_seg.append(word)
            mySave(parse_dir + file_path, ' '.join(ccontent_seg).encode('utf-8'))

    print('分词结束')

if __name__ == '__main__':
    init_stop_words()
    raw_path = '/Users/mac/Desktop/articles/'
    parse_path = '/Users/mac/Desktop/divided_articles/'
    myparse(raw_path, parse_path)

    # raw_path = './mysource/test/raw/'
    # parse_path = './mysource/test/parse/'
    # myparse(raw_path, parse_path)
