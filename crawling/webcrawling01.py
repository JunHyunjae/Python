import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.cgv.co.kr/movies/?ft=0")
c = r.content
html = BeautifulSoup(c, "html.parser")
ol = html.find("ol")
li = ol.find_all("li")

for l in li:
    div = l.find("div", {"class":"box-contents"})
    strong = div.find("strong").text
    print(strong)
    print("-"*50)
