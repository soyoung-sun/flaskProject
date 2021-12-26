from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # render_template 함수는 templates 폴더에 있는 html 파일을 웹브라우저에게 전달
    return render_template('index.html')


if __name__ == '__main__':
    # 플라스크 앱 구동 설정
    app.run('0.0.0.0', port=9000, debug=True)
