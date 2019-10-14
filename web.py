import base64

from flask import Flask, jsonify, request
from config import Config
from ocr.ml_predict import Predict

app = Flask(__name__)


class Web:
    def run(self):
        app.run(**Config.WEB)


@app.route('/check', methods=['POST'])
def check():
    img = request.form.get('img')
    try:
        img = base64.b64decode(img)
    except Exception as e:
        pass
    if not img:
        return jsonify({'msg': 'Wrong format. '})
    result = Predict.share().get_coordinate(img)
    return jsonify({
        'msg': 'success',
        'result': result
    })


if __name__ == '__main__':
    Web().run()
