import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

def get_daily_bible_reading():
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d") # 오늘의 날짜를 가져옵니다
    today1 = datetime.now(timezone(timedelta(hours=9))).strftime("%Y.%m.%d (%a)")  # 오늘의 요일을 가져옵니다
    today1 = today1.replace('Mon', '월').replace('Tue', '화').replace('Wed', '수').replace('Thu', '목').replace('Fri', '금').replace('Sat', '토').replace('Sun', '일')

    print(today1 + "\n")  # 오늘의 날짜와 요일을 출력합니다

    resp = requests.get('https://www.duranno.com/qt/view/bible.asp?qtDate=' + today)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    titleTag = soup.select('h1 span')

    for element in titleTag:
        title = element.get_text()
        print(title)

    bibleTag = soup.select('h1 em')
    for element in bibleTag:
        bible = element.get_text()
        print(bible)

    # 페이지에서 모든 제목(title) 태그를 찾습니다.
    titles = soup.find_all('p', class_='title')

    for title in titles:
        section_title = title.get_text().strip()

        # "오늘의 찬송"과 "묵상 도우미" 섹션은 무시하고 크롤링합니다.
        if section_title == "오늘의 찬송" or section_title == "묵상 도우미":
            continue

        print("\n" + section_title + "\n")

        # 각 섹션의 시작과 끝을 확인하여 크롤링합니다.
        section_html = ''
        current_element = title.find_next()
        while current_element and current_element.name != 'p' and 'title' not in current_element.get('class', []):
            section_html += str(current_element)
            current_element = current_element.find_next()

        # 섹션의 HTML 코드를 파싱하고 표(tr)에서 th와 td의 내용을 출력합니다.
        section_soup = BeautifulSoup(section_html, 'html.parser')
        tables = section_soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    print(th.get_text() + " " + td.get_text())

# 함수 호출
get_daily_bible_reading()
