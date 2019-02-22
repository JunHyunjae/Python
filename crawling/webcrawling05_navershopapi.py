import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import os


client_id = "OoBs9usFBTzJKxJ9K8Py"
client_secret = "wSyAyJDQi0"
encText = urllib.parse.quote("brand b 뉴마이펫키트")
url ="https://openapi.naver.com/v1/search/shop.json?query=" + encText + "&display=2&sort=asc"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode==200:
    response_body = response.read()
    data = response_body.decode('utf-8')
else:
    print("Error Code:" + rescode)


'''
with open(data,"r", encoding="utf8") as f :
    contents = f.read()                                # contents에는  string  으로 저장됨.
    json_data = json.loads(contents)      # 바로 이부분이 핵심인데, 이부분에서 json을 python의 자료형으로 바꿔줌
    print(json_data["display"])
    print(json_data["items"][0])
'''

#print(data)
output = json.loads(data)
print(output)
print(output['items'][0]['lprice'])
