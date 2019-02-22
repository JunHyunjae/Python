import requests, operator, pandas, glob2, datetime, nltk
from bs4 import BeautifulSoup
from matplotlib import font_manager, rc
from konlpy.tag import Twitter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def crawlingData(date, pageCount):
    now = datetime.datetime.now()
    l = []

    for pagecount in range(1, int(pageCount)):
        r = requests.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date="
                         + str(date) + "&page=" + str(pagecount))
        c = r.content
        html = BeautifulSoup(c, "html.parser")
        all = html.find_all("li")

        for item in all:
            for item2 in item.find_all("dl"):
                d = {}

                try:
                    linkTag = item2.find("dt", {"class": ""}).find("a")
                    d["LinkSrc"] = linkTag['href']
                    d["Title"] = linkTag.text.replace("\t", "").replace("\n", "").replace("\r", "")[1:len(linkTag.text)+1]

                except:
                    d["LInkSrc"] = None
                    d["Title"] = None

                try:
                    contentTag = item2.find("dd")
                    d["Content"] = contentTag.text.replace("\t", "").replace("\n", "").replace("\r", "").replace(",", "").replace('"', "").split("…")[0]
                    d["Company"] = contentTag.find("span", {"class": "writing"}).text
                    d["Date"] = contentTag.find("span", {"class": "date"}).text

                except:
                    d["Content"] = None
                    d["Company"] = None
                    d["Date"] = None

                l.append(d)

        df = pandas.DataFrame(l)
        df.to_csv('%s-%s-%s-%s-%s-%s.csv' % (now.year, now.month, now.day, now.hour, now.minute, now.second),
                  encoding='utf-8-sig', index=False)


def checkFileName(fileName):
    now = datetime.datetime.now()

    if len(glob2.glob("*.csv")) == 0:
        print("No file found in this directory")
        return -1
    else:
        if fileName == "all":
            result = []
            for i in glob2.glob("*.csv"):
                result.append(pandas.read_csv(i))

            outputFileName = '%s-%s-%s-%s-%s-%s merging.csv' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

            resultDf = pandas.concat(result, ignore_index=True)
            resultDf.to_csv(outputFileName, encoding='utf-8-sig')

            return outputFileName

        else:
            return fileName


def loadFile(fileName):
    outputFileName = checkFileName(fileName)


def analyze(content):
    nouns = t.nouns(str(content))
    ko = nltk.Text(nouns, name="분석")
    ranking = ko.vocab().most_common(100)
    tmpData = dict(ranking)
    wordcloud = WordCloud(relative_scaling=0.2, background_color="white").generate_from_frequencies(tmpData)
    plt.figure(figsize=(16, 8))
    plt.imsow(wordcloud)
    plt.axis("off")
    plt.show()


def mainSetting():
    while(1):
        kb = input("$ ")
        if kb == "exit":
            break
        elif kb == "crawling":
            date = input("Enter news date : ")
            page = input("Enter your pageCount : ")
            crawlingData(date, page)
        elif kb == "loadAll":
            loadFile("all")
        elif kb == "load":
            fileName = input("Enter your csv file name : ")
            loadFile(filename)
        elif kb == "analyze":
            fileName = input("Enter your csv file name : ")
            loadFile(filename, 1)
        else:
            print("command error !")



mainSetting()
#font_name = font_manager.FontProperties(fname="/Library/Fonts/AppleGothic.ttf").get_name()
#rc('font', family=font_name)
#t = Twitter()
#analyze(t)