import sys
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image

# 네이버 뉴스 크롤링
URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = ("&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=26&mynews=0&office_type=0"
                       "&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=")

def get_link(keyword, page_range):  # 매개변수 : 키워드, 페이지 범위
    link = []

    for page in range(page_range):
        current_page = 1 + page * 10  # 네이버 뉴스 URL : 1 -> 11 -> 21 -> 31 ... (1페이지 당 10개 뉴스가 있음)
        crawling_url_list = URL_BEFORE_KEYWORD + keyword + URL_BEFORE_PAGE_NUM + str(current_page)

        # URL에 get 요청을 보냄
        response = requests.get(crawling_url_list)
        # print(response)  # 응답 사인을 출력 (정상 : 200)

        soup = BeautifulSoup(response.text, 'lxml')
        url_tag = soup.select('a.news_tit')

        for url in url_tag:
            link.append(url["href"])

    return link

def get_article(file1, link):  # 매개변수 : 기사를 저장할 파일, 링크

    with open(file1, 'w', encoding='utf8') as f:  # 기사를 저장할 파일을 쓰기 모드로 열기
        for url2 in link:
            article = Article(url2, language="ko")  # 인스턴스 생성

            try:
                article.download()
                article.parse()
            except:
                continue

            news_title = article.title
            news_content = article.text

            f.write(news_title)
            f.write(news_content)

    f.close()  # 파일 닫기

def wordcount(file1, file2):  # 매개변수 : 기사를 저장한 파일, 단어를 저장할 파일
    f = open(file1, "r", encoding="utf8")
    g = open(file2, "w", encoding="utf8")  # 단어와 개수를 저장하는 파일 생성

    engine = Okt()
    data = f.read()
    all_nouns = engine.nouns(data)
    nouns = [n for n in all_nouns if (len(n) > 1)]

    count = Counter(nouns)
    # Dict = {Key : Value} <- t[0] : Key / t[1] : Value
    by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for i, j in zip(word, number):
        final = f"{i}   {j}"
        g.write(final + "\n")

    f.close()
    g.close()

    return by_num, count

def top_n(count, file3):  # 매개변수 : 가장 많이 나온 단어 10개를 저장할 파일
    g = open(file3, "w", encoding="utf8")  # 가장 많이 나온 단어 10개를 저장할 파일을 쓰기 모드로 열기
    rank = count.most_common(10)  # count 값의 요소 중 빈도 수가 높은 순으로 상위 10개 리턴

    word = [i for i in dict(rank).keys()]  # rank를 딕셔너리 형태로 변환 후 Key와 Value를 추출
    number = [i for i in dict(rank).values()]

    for i, j in zip(word, number):  # word, number를 묶어 텍스트 파일에 저장
        final = f"{i}   {j}"
        g.write(final + "\n")

    g.close()
    return rank

def full_vis_bar(by_num):  # 매개변수 : 값을 기준으로 내림차순으로 정렬된 변수

    for w, n in list(by_num.items()):  # by_num의 요소 값이 15 이하이면 딕셔너리에서 키 삭제
        if n <= 15:
            del by_num[w]

    fig = plt.gcf()
    fig.set_size_inches(20, 10)  # 1 -> 100 pixel, 20 -> 2000 pixel
    matplotlib.rc('font', family="Malgun Gothic", size=10)
    plt.title("기사에 나온 전체 단어 개수", fontsize=30)
    plt.xlabel("기사에 나온 단어", fontsize=20)
    plt.ylabel("기사에 나온 단어 개수", fontsize=20)
    plt.bar(by_num.keys(), by_num.values(), color="#6799FF")
    plt.xticks(rotation=45)
    plt.savefig("top_words.jpg")
    plt.show()

def top_n_vis_bar(rank):  # 매개변수 : 빈도 수가 높은 상위 10개를 저장한 딕셔너리
    topn_data = dict(rank)
    fig = plt.gcf()
    fig.set_size_inches(20, 10)  # 1 -> 100 pixel, 20 -> 2000 pixel
    matplotlib.rc('font', family="Malgun Gothic", size=10)
    plt.title("기사에 나온 10개 단어 개수", fontsize=30)
    plt.xlabel("기사에 나온 단어", fontsize=20)
    plt.ylabel("기사에 나온 단어 개수", fontsize=20)
    plt.bar(topn_data.keys(), topn_data.values(), color="red")
    plt.xticks(rotation=45)
    plt.savefig("top_words.jpg")
    plt.show()

def wordcloud(by_num):
    masking_image = np.array(Image.open("alice_mask.png"))
    wc = WordCloud(font_path="malgun", background_color="white", width=2500, height=1500, mask=masking_image)
    cloud = wc.generate_from_frequencies(by_num)
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wordcloud.jpg")
    plt.show()

def main(argv):
    link = get_link(argv[1], int(argv[2]))
    get_article("수집내용.txt", link)
    by_num, count = wordcount("수집내용.txt", "wordcount.txt")
    full_vis_bar(by_num)
    rank = top_n(count, "상위 10개 단어.txt")
    top_n_vis_bar(rank)
    wordcloud(by_num)

if __name__ == "__main__":
    main(sys.argv)