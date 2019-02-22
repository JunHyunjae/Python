import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3


def make_db():
    r = requests.get("https://www.suto.co.kr/bbs/board.php?bo_table=cpevent")
    c = r.content

    con = sqlite3.connect("event.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test(Title text, Link text, ExpiredDate text)")

    soup = BeautifulSoup(c, 'html.parser')
    area = soup.find_all("td", {"class": "td_subject"})

    for t in area:
        a = t.find("a")
        link = a['href']
        title = a.text

        content = requests.get(link).content
        soup = BeautifulSoup(content, 'html.parser')

        item_box =  soup.find("div", {"class": "item-box"})

        try:
            li = item_box.find_all("li")
            t = li[3]
            s = t.text
            s = s.split(' ')

            convert_date = datetime.strptime(s[2], "%Y-%m-%d").date() # 문자열을 date 객체로 변환
            convert_date2 = datetime.strptime(s[2], "%Y-%m-%d") # 문자열을 datetime 객체로 변환

            #print(convert_date)
            #print(type(convert_date))

            cursor.execute("INSERT INTO test VALUES(?,?,?)", (title, link, convert_date))
            con.commit()

        except:
            print("item-optin 없음.")


    con.close()


def read_db():
    con = sqlite3.connect("event.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM test")
    #print(cursor.fetchall())
    print(cursor.fetchone()[0])



def update_crawling():
    con = sqlite3.connect("event.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM test")

    r = requests.get("https://www.suto.co.kr/bbs/board.php?bo_table=cpevent")
    c = r.content

    soup = BeautifulSoup(c, 'html.parser')
    area = soup.find_all("td", {"class": "td_subject"})
    latest = cursor.fetchone()[0]

    for idx, t in enumerate(area):
        a = t.find("a")
        link = a['href']
        title = a.text

        if idx>2:
            if latest == title:
                break
            else:
                content = requests.get(link).content
                soup = BeautifulSoup(content, 'html.parser')

                item_box =  soup.find("div", {"class": "item-box"})

                try:
                    li = item_box.find_all("li")
                    t = li[3]
                    s = t.text
                    s = s.split(' ')

                    convert_date = datetime.strptime(s[2], "%Y-%m-%d").date() # 문자열을 date 객체로 변환

                    print(title)
                    print(link)
                    print(convert_date)
                    #print(type(convert_date))

                    cursor.execute("INSERT INTO test VALUES(?,?,?)", (title, link, convert_date))
                    con.commit()

                except:
                    print("item-optin 없음.")

    con.close()


#make_db()
update_crawling()
#read_db()