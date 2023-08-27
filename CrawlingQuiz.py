import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = ("&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=26&mynews=0&office_type=0"
                       "&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=")

def search():
    print("수집할 키워드를 입력하세요. : ", end='')
    keyword = input()
    print("수집할 페이지 개수를 입력하세요. : ", end='')
    page_num = int(input())

    driver = webdriver.Chrome()
    driver.get("https://www.naver.com")

    keywordSearch = driver.find_element(By.CLASS_NAME, "search_input")
    keywordSearch.send_keys(keyword)

    driver.find_elements(By.CLASS_NAME, "btn_search")[0].click()
    driver.find_element(By.LINK_TEXT, "뉴스").click()

    return keyword, page_num

def get_link(keyword, page_num):
    link = []

    for page in range(page_num):
        current_page = 1 + page * 10
        crawling_url_list = URL_BEFORE_KEYWORD + keyword + URL_BEFORE_PAGE_NUM + str(current_page)

        response = requests.get(crawling_url_list)

        soup = BeautifulSoup(response.text, 'lxml')
        url_tag = soup.select('a.news_tit')

        for url in url_tag:
            link.append(url["href"])

    return link

def get_article(link):
    news_title = []
    news_content = []

    for url in link:
        article = Article(url, language="ko")

        try:
            article.download()
            article.parse()
        except:
            article.title = ''
            article.text = ''

        news_title.append(article.title)
        news_content.append(article.text)

    return news_title, news_content

def wordcount(news_content):
    topWord = []
    engine = Okt()
    for i in news_content:
        all_nouns = engine.nouns(i)
        nouns = [n for n in all_nouns if (len(n) > 1)]
        rank = Counter(nouns).most_common(5)
        word = [i for i in dict(rank).keys()]
        topWord.append(word)

    return topWord

def main():

    keyword, page_num = search()
    link = get_link(keyword, page_num)
    news_title, news_content = get_article(link)
    top_word = wordcount(news_content)

    df = pd.DataFrame({"제목" : news_title, "본문" : news_content, "기사 URL" : link, "Top 5 단어" : top_word}).to_csv('news.csv', index=False)

if __name__ == "__main__":
    main()