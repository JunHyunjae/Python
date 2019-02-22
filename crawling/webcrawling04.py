import requests, operator, pandas, glob2, datetime, nltk
from bs4 import BeautifulSoup
from collections import OrderedDict
import urllib.request as req
import re


def no_space(text):
    text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
    text2 = re.sub('\n\n', '', text1)
    return text2


def print_title(final_url):
    if final_url == None:
        print(None)
    else:
        print("final_url: ", final_url)
        res = req.urlopen(final_url)
        soup = BeautifulSoup(res, 'html.parser')
        try:
            title = soup.find("div", {"class": "se_textView"}).find_all("h3", {"class": "se_textarea"})

        except:
            title = soup.find("div", {"class": "htitle"}).find_all("span", {"class": "pcol1 itemSubjectBoldfont"})

        for a in title:
            text = a.get_text()
            text2 = no_space(text)

        text2 = text2.lstrip().rstrip()

        print("{0} {1}\n".format('[title]', text2))


def get_final_url(input_url):
    try:
        print("input_url : ", input_url)
        url_1 = str(input_url)
        html_result = requests.get(url_1)
        soup_temp = BeautifulSoup(html_result.text, 'html.parser')
        area_temp = soup_temp.find(id='screenFrame')
        url_2 = area_temp.get('src')
        print("1. screenFrame_url : ", url_2)

    except:
        try:
            area_temp = soup_temp.find(id='mainFrame')
            url_3 = area_temp.get('src')
            url_4 = "https://blog.naver.com/" + url_3
            print("2. mainFrame_url : ", url_4)
            return url_4
        except:
            return None

    try:
        html_result = requests.get(url_2)
        soup_temp = BeautifulSoup(html_result.text, 'html.parser')
        area_temp = soup_temp.find(id='mainFrame')
        url_3 = area_temp.get('src')
        url_4 = "https://blog.naver.com/" + url_3
        print("3. mainFrame_url : ", url_4)
        return url_4

    except:
        print("error")
        return None


def test():
    # search_word = str(input("검색어를 입력하시오: "))
    search_word = "괌"
    url = "https://search.naver.com/search.naver"
    header = {'User-Agent': 'Mozila/5.0', 'referer': 'http://www.naver.com'}
    # naver에서 검색한 것 처럼 헤더를 달아주면 forbidden 403 에러를 막을 수 있다.

    post_dict = OrderedDict()
    print(post_dict)
    cnt = 1

    for page in range(1, 100):
        param = {
            'where': 'post',
            'query': search_word,
            'date_from': '20180101',
            'date_to': '20181030',
            'date_option': '8',
            'start': (page - 1) * 10 + 1,
        }

        print("페이지 : ", page)

        response = requests.get(url, params=param, headers=header)
        print(response)
        print(response.url)
        #        print(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')

        area = soup.find("div", {"class": "blog section _blogBase"}).find_all("a", {"class": "url"})

        for tag in area:
            sub_url = tag["href"]
            print_title(get_final_url(sub_url))

            if tag['href'] in post_dict:
                print('마지막 페이지 마지막 블로그 입니다.')
                exit()

            post_dict[tag['href']] = tag.text
            cnt += 1

    '''
    for tag in area:
        t = tag.get("href")
        print(t)
    '''


test()
