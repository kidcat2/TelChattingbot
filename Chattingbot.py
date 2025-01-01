import telegram.update
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from upbitpy import Upbitpy
import datetime

# chrome을 안보이는 모드로 실행하기 위한 코드
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
#

def wrong_command():  # 잘못된 명령어를 입력한 경우
    response_all = ["잘못된 명령어입니다.", "잘 모르겠습니다 ㅠㅜ", "무엇을 원하시나요?", "다시 한 번 알려주세요."]
    response = random.choice(response_all)
    return response


def check_command():  # 명령어 재확인
    command_message = '''
        <명령어 목록>

    - "공지" : 전북대학교 공지사항을 확인할 수 있습니다.

    - "날씨 + 지역" : 알고싶은 지역의 날씨를 알려드립니다. ex) 날씨 전주, 날씨 서울

    - "뉴스" : 실시간 헤드라인 뉴스를 가져옵니다.
    
    - "이슈" : 요즘 핫한 이슈를 알려드립니다.

    - "유튜브" : 유튜브(YOUTUBE) 실시간 인기 동영상을 보여드립니다.
    
    - "코인시세" : 비트코인(BTC), 이더리움(ETH), 리플(XRP) 코인의 실시간 시세를 알려드립니다.

    - "IT" or 'it' : IT지능정보공학과 공지사항을 보여드립니다. 

    - 명령어를 다시 보고 싶으시면 '명령어'를 입력해주세요.'''
    return command_message


def hot_issue_daum():  # 다음 카페의 핫 이슈 가져오기
    driver = webdriver.Chrome("/Users/admin/Downloads/chromedriver", options=options)
    driver.get('https://top.cafe.daum.net/')
    driver.implicitly_wait(10)
    retitle = driver.find_elements(By.CLASS_NAME, "desc_info")
    relink = driver.find_elements(By.CLASS_NAME, "link_popular")

    hot_issue = []
    for i in range(5):
        hot_issue.append(retitle[i].text + "\n" + relink[i].get_attribute('href'))

    driver.quit()
    return hot_issue

def crpyto_price():  # 가장 거래량이 많은 3대 암호화폐의 현재 원화 가격(업비트 거래소 기준)
    upbit = Upbitpy()

    tickerBTC = upbit.get_ticker(['KRW-BTC'])[0]
    price_BTC = format(int(tickerBTC['trade_price']), ',')
    tickerETH = upbit.get_ticker(['KRW-ETH'])[0]
    price_ETH = format(int(tickerETH['trade_price']), ',')
    tickerXRP = upbit.get_ticker(['KRW-XRP'])[0]
    price_XRP = format(int(tickerXRP['trade_price']), ',')

    text1 = '3대 코인 현재 원화 가격(업비트 기준)입니다.'
    text2 = '({}) 비트코인 가격: {} 원'.format(datetime.datetime.now().strftime('%m/%d %H:%M:%S'), price_BTC)
    text3 = '({}) 이더리움 가격: {} 원'.format(datetime.datetime.now().strftime('%m/%d %H:%M:%S'), price_ETH)
    text4 = '({}) 리플 가격: {} 원'.format(datetime.datetime.now().strftime('%m/%d %H:%M:%S'), price_XRP)
    text = text1 + "\n" + text2 + "\n" + text3 + "\n" + text4
    return text

def hot_youtube():  # 유튜브 실시간 인기 동영상
    driver = webdriver.Chrome("/Users/admin/Downloads/chromedriver", options=options)
    driver.get('https://www.youtube.com/feed/trending')
    driver.implicitly_wait(10)
    retitle = driver.find_elements(By.ID, "video-title")
    title = []

    for i in range(3):
        title.append(retitle[i].text + "\n" + retitle[i].get_attribute('href'))
    driver.quit()
    return title

def weather_crawling(area):  # 네이버 날씨
    html = requests.get('https://search.naver.com/search.naver?query=' + area + '+날씨')
    soup = BeautifulSoup(html.text, 'html.parser')
    data1 = soup.find('div', {'class': 'weather_info'})
    if data1 == None:
        weather_fail = "올바른 지역을 입력해주세요."
        return weather_fail
    else:
        data2 = data1.findAll('dd') 
        feel_temperature = data2[0].text  # 오늘 온도
        humidity = data2[1].text  # 오늘 습도
        wind = data2[2].text  # 오늘 풍속
        whole_temp = "온도 : " + feel_temperature + "\n" + "습도 : " + humidity + "\n" + "풍속 : " + wind
        return whole_temp

def jeonbuk_notice():  # 전북대 공지
    html = requests.get('https://www.jbnu.ac.kr/kor/?menuID=139')
    soup = BeautifulSoup(html.text, 'html.parser')
    data1 = soup.find('div', {'class': 'page_list'})
    data2 = data1.findAll('a')
    data4 = "\n"
    link = []
    link = jeonbuk_notice_link()
    date = []
    date = jeonbuk_notice_date()
    count = 1
    for i in range(len(data2)):
        data3 = data2[i].text
        data3 = data3.strip()
        if (len(data3) > 3):
            data4 = data4 + "\n" + "\n" + str(count) + ". " + data3 + "   [작성일 : " + date[count - 1] + "]" + "\n" + \
                    link[count - 1]
            count = count + 1
            print("\n")
    return data4

def jeonbuk_notice_date():  # 전북대 공지 게시일
    html = requests.get('https://www.jbnu.ac.kr/kor/?menuID=139')
    soup = BeautifulSoup(html.text, 'html.parser')
    data1 = soup.find('div', {'class': 'page_list'})
    data2 = data1.findAll("td", {'class': 'mview'})  # td 태그의 mview 클라스를 전부 가져옴
    date = []
    for i in range(len(data2)):  # mview 를 루프하면서 2022 가 들어간 스트링만 골라서 list date 에 저장
        data4 = data2[i].text
        if "2022" in data4:
            date.append(data4)
    return date

def jeonbuk_notice_link():  # 전북대 공지 링크
    html = requests.get('https://www.jbnu.ac.kr/kor/?menuID=139')
    soup = BeautifulSoup(html.text, 'html.parser')
    data1 = soup.find('div', {'class': 'page_list'})
    data2 = data1.findAll("td", {'class': 'left'})  # td 태그의 mview 클라스를 전부 가져옴
    # print(data2)
    list_link = []
    for i in range(len(data2)):
        list_link.append("https://www.jbnu.ac.kr/kor/" + data2[i].findAll('a')[0].attrs['href'])

    return list_link

def itnotice_all():  # it정보공학과 공지 (총합)
    html = requests.get('https://it.jbnu.ac.kr/it/9841/subview.do')
    soup = BeautifulSoup(html.text, 'html.parser')
    data1 = soup.find('table', {'class': 'artclTable artclHorNum1'})
    data2 = data1.findAll('strong')
    data3 = data1.findAll("td", {'class': '_artclTdRdate'})
    it_date = []
    for i in range(len(data3)):
        it_date.append(data3[i].text)
    notice = []
    count = 1
    for i in range(len(data2)):
        notice_data = str(count + i) + ". " + data2[i].text + "  <작성일 : " + it_date[i] + ">" + "\n"
        notice.append(notice_data)
        print("\n")
    return notice

def news_crawl():    #헤드라인 뉴스
    res = requests.get("https://media.naver.com/press/001")
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    news_list = soup.find("ul", attrs={"class": "press_news_list as_bottom"}).find_all("li", limit=4)
    data = []
    for index, news in enumerate(news_list):
        title = news.find("span").get_text().strip()
        link = news.find("a")["href"]
        data.append(title + "\n" + str(link))
    return data


token = "5315245248:AAGSiFMWJaPQxwSsopEVUufmEUwvqLiHLDs"
id = -1001672093048  # 고정 id를 받게 하는법 , 아래 코드에 가장 최근 chat id 를 가져오는 법을 적어뒀습니다.
bot = telegram.Bot(token=token)

# 봇이 나에게 메시지를 출력하게 하는 방법
# bot.sendMessage(chat_id=id, text="테스트 중입니다.") # chat id 가 id라면, text 를 출력한다.

# 사용자가 입력하는 메시지를 받아들이기 위한 선행 코드
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

# info_message 에 할말을 저장해놓고, sendMessage를 통해 바로 출력합니다.
descryption_message = '''

  전북대 채팅 봇 부기(Boogie)입니다!

  한 가지 기능만을 제공하는 봇이 아닌 여러가지 일상생활에서 필요한 기능들을 구현하는 다기능 봇입니다.

  날씨, 뉴스, 전북대학교 공지사항, 유튜브 인기동영상, 핫이슈, 코인시세, 학과 공지사항 등을 알려드립니다.

  관련 명령어를 알고 싶으시면 '명령어' 를 입력해주세요.

  '''

bot.sendMessage(chat_id=id, text=descryption_message)

def handler(update, context):
    user_text = update.message.text  # 사용자가 입력한 message 를 user text 에 저장합니다.

    if "날씨" in user_text:
        area = user_text[3:]
        weather_now = weather_crawling(area)
        if weather_now == "올바른 지역을 입력해주세요!":
            bot.send_message(chat_id=id, text=weather_now)
        else:
            bot.send_message(chat_id=id, text="오늘 " + area + " 날씨입니다.")
            bot.send_message(chat_id=id, text=weather_now)

    elif user_text == "명령어":
        command_message = check_command()
        bot.send_message(chat_id=id, text=command_message)

    elif user_text == "공지":
        notice = jeonbuk_notice()
        bot.send_message(chat_id=id, text=notice)

    elif (user_text == "IT") or (user_text == "it"):
        it_notice = itnotice_all()
        notice_union = "\n"
        for i in range(len(it_notice)):
            notice_union = notice_union + it_notice[i] + "\n"
        bot.send_message(chat_id=id, text=notice_union)

    elif user_text == "코인시세":
        crpyto = crpyto_price()
        bot.send_message(chat_id=id, text=crpyto)

    elif user_text == "뉴스":
        news = news_crawl()
        for i in range (len(news)) :
            bot.send_message(chat_id=id, text=news[i])

    elif user_text == "유튜브":
        bot.send_message(chat_id=id, text="검색중입니다... 조금만 기다려주세요.")
        youtube = hot_youtube()
        for i in range(3):
            bot.send_message(chat_id=id, text=youtube[i])

    elif user_text == "이슈":
        bot.send_message(chat_id=id, text="검색중입니다... 조금만 기다려주세요.")
        daum_hot = hot_issue_daum()
        for i in range(5):
            bot.send_message(chat_id=id, text=daum_hot[i])

    else:
        response = wrong_command()
        bot.send_message(chat_id=id, text=response)


echo_handler = MessageHandler(Filters.text, handler)  
dispatcher.add_handler(echo_handler)  


