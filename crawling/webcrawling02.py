import requests
from bs4 import BeautifulSoup

# ul class:type06_headline -> li -> dl -> dt.text


def getImageSrc():
    dl = all.find_all("dl")
    for item2 in dl:
        try:
            img = item2.find("dt", {"class": "photo"}).find("img")
            print(img['src'])
        except:
            print("No image")


def getLinkandTitle():
    dl = all.find_all("dl")
    for item in dl:
        link = item.find("dt", {"class": ""}).find("a")
        print(link['href'])
        print(link.text.replace("\t", "").replace("\n", ""))
        #print(link.text.replace("\t", "").replace("\n", "")[1:len(link.text) + 1])


def getContent():
    dl = all.find_all("dl")
    for item in dl:
        try:
            content = item.find("dd")
            print(content.text.replace("\t", "").replace("\n", "").split("…"))
            print(content.text.replace("\t", "").replace("\n", "").split("…")[0])
            print(content.find("span", {"class": "writing"}).text)
            print(content.find("span", {"class": "date is_new"}).text)
        except:
            print("No Content")


r = requests.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100")
c = r.content
html = BeautifulSoup(c, "html.parser")
all = html.find("ul", {"class": "type06_headline"})

getImageSrc()
print("="*50)
getLinkandTitle()
print("="*50)
getContent()