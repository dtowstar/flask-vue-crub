from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# @app.route('/', methods=['GET'])
# def ping_pong():
#   return jsonify("FHASDKF")  # （jsonify返回一个json格式的数据）


app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/confirmPage', methods=('GET', 'POST'))
def login():
    homepage = ''
    if request.method == 'POST':
        homepage = request.json.get('form.homepage')
        print(homepage)
        return jsonify("true")
    else:
        return jsonify("false")


if __name__ == '__main__':
    app.run()
