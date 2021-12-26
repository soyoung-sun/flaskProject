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
    result = {
        'result': 'success',
        'msg': 'test'
    }
    return jsonify(result)


@app.route('/memo', methods=['POST'])
def post_article():
    # ajax 사용해서 전송하는 data 정보는 request.form 변수에 저장됨.
    # print(request.form.get('url_give'))
    # print(request.form.get('comment_give'))
    memo = {
        'url': request.form.get('url_give'),
        'comment': request.form.get('comment_give'),
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
