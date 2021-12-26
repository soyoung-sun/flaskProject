import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.alonememo


@app.route('/')
def hello_world():  # put application's code here
    # render_template 함수는 templates 폴더에 있는 html 파일을 웹브라우저에게 전달
    return render_template('index.html')


@app.route('/memo')
def show_articles():
    articles = db.article.find({}, {'_id':False})

    result = {
        'result': 'success',
        'articles': list(articles)
    }

    print(result)

    return jsonify(result)


@app.route('/memo', methods=['POST'])
def post_article():
    # ajax 사용해서 전송하는 data 정보는 request.form 변수에 저장됨.
    # print(request.form.get('url_give'))
    # print(request.form.get('comment_give'))
    url = request.form.get('url_give')

    # 크롤링할 때 웹브라우저 호출인 것으로 위장
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    crawling_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(crawling_data.text, 'html.parser')

    og_img_url = soup.select_one('meta[property="og:image"]')['content']
    og_title = soup.select_one('meta[property="og:title"]')['content']
    og_description = soup.select_one('meta[property="og:description"]')['content']

    memo = {
        'url': url,
        'comment': request.form.get('comment_give'),
        'img_url': og_img_url,
        'title': og_title,
        'description': og_description,
    }

    # MongoDB 저장
    db.article.insert_one(memo)

    result = {
        'result': 'success',
        'msg': '저장 완료'
    }
    return jsonify(result)

if __name__ == '__main__':
    # 플라스크 앱 구동 설정
    app.run('0.0.0.0', port=9000, debug=True)
