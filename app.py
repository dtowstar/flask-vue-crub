from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openhome import open


# @app.route('/', methods=['GET'])
# def ping_pong():
#   return jsonify("FHASDKF")  # （jsonify返回一个json格式的数据）


app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/confirmPage', methods=('GET', 'POST'))
def login():
    homepage = request.json.get('form.homepage')
    if request.method == 'POST':
        print(homepage)
        open()
        return jsonify("true")
    else:
        return jsonify("false")


if __name__ == '__main__':
    app.run()
