import bs4, requests, os, datetime, time

root_dir = '/Users/mac/Desktop/articles/'

def fetch_URL(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    r = requests.get(url,headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def getKindList(year, month, day):
    kind_names = []
    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'
    html = fetch_URL(url)
    bsobj = bs4.BeautifulSoup(html,'html.parser')
    # hi = bsobj.find('div', attrs = {'href': 'pageLink'})
    # print(bsobj)
    # a = 1 / 0
    pageList = bsobj.find('div', attrs = {'class': 'swiper-container'}).find_all('div', attrs = {'class': 'swiper-slide'})
    kind_linkList = []
    
    for page in pageList:
        link = page.a["href"]
        raw_name = str(page.a)
        kind_index = raw_name.index('>') + 1
        half_name = raw_name[kind_index:]
        half_index = half_name.index('<')
        kind_name = half_name[:half_index]
        kind_names.append(kind_name)
        kind_dir = root_dir + kind_name
        if not os.path.exists(kind_dir):
            os.mkdir(kind_dir)
        url = 'http://paper.people.com.cn/rmrb/html/'  + year + '-' + month + '/' + day + '/' + link
        kind_linkList.append(url)
    return kind_linkList, kind_names

def getTitleList(year, month, day, pageurl):
    html = fetch_URL(pageurl)
    bsobj = bs4.BeautifulSoup(html,'html.parser')
    titleList = bsobj.find('div', attrs = {'class': 'news'}).ul.find_all('li')
    # tt = titleList
    # print(titleList)
    titles = []
    titleLinkList = []
    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp['href']
            if 'nw.D110000renmrb' in link:
                url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
                titleLinkList.append(url)
                raw_title = str(temp)
                _index = raw_title.index('>') + 1
                half_title = raw_title[_index:]
                _index = half_title.index('<')
                this_title = half_title[:_index]
                
                titles.append(this_title)
                
                
    return titleLinkList, titles

def resolve_html_str(s):
    _index = s.index('>') + 1
    half_ans = s[_index:]
    _index = half_ans.index('<')
    ans = half_ans[:_index]
    return ans

def saveContent(titleurl, save_dir):
    html = fetch_URL(titleurl)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    article = bsobj.find('div', attrs={'class': 'article'})
    
    title3 = article.find('h3')
    title2 = article.find('h2')
    title1 = article.find('h1')
    
    content = ''
    s1 = resolve_html_str(str(title3))
    if len(s1) != 0:
        content = content + s1 + '\n'
    s2 = resolve_html_str(str(title2))
    if len(s2) != 0:
        content = content + s2 + '\n'
    s3 = resolve_html_str(str(title1))
    if len(s3) != 0:
        content = content + s3 + '\n'
    
    content_list = article.find('div', attrs={'id': 'ozoom'}).find_all('p')
    
    for i in content_list:
        # tmp = str(i)
        # _index = tmp.index('>') + 1
        # temp0 = tmp[_index:]
        # _index = temp0.index('<')
        # content += temp0[:_index] + '\n'
        content = content + resolve_html_str(str(i)) + '\n'
    with open(save_dir, 'w') as outfile:
        outfile.write(content)
    # print(content_list)
    
def save_info(kind_names, all_titles, kind_linkList, all_title_linklist, title_dir, artinfo_dir):
    with open(title_dir, 'w') as fout:
        for i in range(len(kind_names)):
            fout.write(kind_names[i])
            fout.write(' ')
            fout.write(kind_linkList[i])
            fout.write('\n')
        

        # for i in range(len(kind_names)):
    fout.close
    # with open(artinfo_dir, 'w') as fout:
    #     for i in range(len(all_titles)):
    #         for j in range(len(all_titles[i])):
    #             fout.write(all_titles[i][j])
    #             fout.write(' ')
    #             fout.write(all_title_linklist[i][j])
    #             fout.write('\n')
    # fout.close
    with open(artinfo_dir, 'w') as fout:
        for i in range(len(all_titles)):
            fout.write(kind_names[i])
            
            fout.write('\n')
            for j in range(len(all_titles[i])):
                fout.write(all_titles[i][j])
                fout.write(' ')
                fout.write(all_title_linklist[i][j])
                fout.write('\n')
    fout.close


if __name__ == '__main__':
    # ret = fetch_URL('http://paper.people.com.cn/rmrb/html/2021-05/26/nw.D110000renmrb_20210526_1-13.htm')
    # print(ret)
    
    year = '2021'
    month = '04'
    date = '28'
    kind_linkList, kind_names = getKindList(year, month, date)
    # tt_kind_linkList, tt_kindnames = getKindList('2021', '05', '26')
    # print(kind_names)
    all_titles = []
    # print(kind_linkList)
    all_title_linklist = []
    print(f'{len(kind_linkList)} kind_linklist  finished')
    for i in range(len(kind_linkList)):
        
        this_title_linkList, this_titles = getTitleList(year, month, date, kind_linkList[i])
        # tt_title_linkList, tt_titles = getTitleList('2021', '05', '26', tt_kind_linkList[i])
        # this_title_linkList = this_title_linkList + tt_title_linkList
        # this_titles = this_titles + tt_titles

        all_title_linklist.append(this_title_linkList)
        all_titles.append(this_titles)
        # print(f'{i} finished')
    
    cnt = 0
    for i in range(len(all_titles)):
        cnt += len(all_titles[i])
    print(cnt)
    # print(all_title_linklist[1][0])
    for i in range(len(all_title_linklist)):
        kind_dir = root_dir 
        for j in range(len(all_title_linklist[i])):
            this_link = all_title_linklist[i][j]
            this_dir = root_dir + kind_names[i] + '/' + str(j) + '.txt'
            
            saveContent(all_title_linklist[i][j],this_dir)
    title_dir = '/Users/mac/Desktop/title_link.txt'
    artinfo_dir = '/Users/mac/Desktop/article_link.txt'
    save_info(kind_names, all_titles, kind_linkList, all_title_linklist, title_dir, artinfo_dir)