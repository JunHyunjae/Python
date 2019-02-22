import telegram

my_token = '622779547:AAGAUa0a1huyHXA7Cz10U1SYXKakkmyBRBI'

bot = telegram.Bot(token= my_token)

updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.

for u in updates :   # 내역중 메세지를 출력합니다.
    print(u.message)


print(updates)

chat_id = bot.getUpdates()[-1].message.chat.id #가장 최근에 온 메세지의 chat id를 가져옵니다
bot.sendMessage(chat_id = chat_id, text="저는 봇입니다.")