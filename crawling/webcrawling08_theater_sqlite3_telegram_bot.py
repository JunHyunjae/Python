import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import telegram
from apscheduler.schedulers.blocking import BlockingScheduler



def cgv_make_db():
    r = requests.get("http://www.cgv.co.kr/culture-event/event/?menu=2#1")
    c = r.content

    con = sqlite3.connect("theater_event.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test(Title text, Link text, ExpiredDate text, PostDate timestamp)")

    soup = BeautifulSoup(c, 'html.parser')
    area = soup.find_all("td", {"class": "td_subject"})


    for t in reversed(area):
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

            now = datetime.now()

            print("ExpiredDate: ", convert_date)
            print("now : ", now)
            #print(type(convert_date))

            cursor.execute("INSERT INTO test VALUES(?,?,?,?)", (title, link, convert_date, now))
            con.commit()

        except:
            print("item-optin 없음.")


    con.close()


def insert_db():
    con = sqlite3.connect("event.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = con.cursor()
    now = datetime.now()
    cursor.execute("INSERT INTO test VALUES(?,?,?,?)", ('[키즈현대] 어린이 안전짱 안전증 인증 이벤트(BHC치킨,배라파인트)', 'https://www.suto.co.kr/bbs/board.php?bo_table=cpevent&wr_id=69069', '2019-02-15', now))
    con.commit()
    con.close()



def read_db():
    con = sqlite3.connect("event.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM test ORDER BY PostDate")
    #print(cursor.fetchall())
    print(cursor.fetchone())
    #print(cursor.fetchone()[0])




def update_crawling():
    my_token = '622779547:AAGAUa0a1huyHXA7Cz10U1SYXKakkmyBRBI'
    bot = telegram.Bot(token=my_token)
    updates = bot.getUpdates()  # 업데이트 내역을 받아옵니다.
    chat_id = bot.getUpdates()[-1].message.chat.id  # 가장 최근에 온 메세지의 chat id를 가져옵니다

    con = sqlite3.connect("event.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM test ORDER BY PostDate DESC")

    r = requests.get("https://www.suto.co.kr/bbs/board.php?bo_table=cpevent")
    c = r.content

    soup = BeautifulSoup(c, 'html.parser')
    area = soup.find_all("td", {"class": "td_subject"})
    latest = cursor.fetchone()[0]
    print("Latest : ", latest)

    area = area[3:]

    for idx, t in enumerate(area):
        a = t.find("a")
        link = a['href']
        title = a.text
        if title == latest:
            break

    area = area[:idx]

    for t in reversed(area):
        a = t.find("a")
        link = a['href']
        title = a.text
        content = requests.get(link).content
        soup = BeautifulSoup(content, 'html.parser')
        item_box = soup.find("div", {"class": "item-box"})

        try:
            li = item_box.find_all("li")
            t = li[3]
            s = t.text
            s = s.split(' ')

            convert_date = datetime.strptime(s[2], "%Y-%m-%d").date()  # 문자열을 date 객체로 변환
            now = datetime.now()

            print(title)
            print(link)
            print(convert_date)

            cursor.execute("INSERT INTO test VALUES(?,?,?,?)", (title, link, convert_date, now))
            # DB에 반영
            con.commit()

            bot.sendMessage(chat_id=chat_id, text=title)
            bot.sendMessage(chat_id=chat_id, text=link)

        except:
            print("item-optin 없음.")



    con.close()





if __name__ == '__main__':
    scheduler = BlockingScheduler()
    print("START!")
    scheduler.add_job(update_crawling, 'interval', seconds=900, )
    print("END!")

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        print("END!")
        pass

#make_db()
# update_crawling()
# read_db()
# insert_db()