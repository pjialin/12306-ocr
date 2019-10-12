import base64

from sanic import Sanic
from sanic.response import json

from config import Config
from ocr.ml_predict import Predict

app = Sanic()


class Web:
    async def run(self):
        await app.create_server(return_asyncio_server=True, **Config.WEB)


@app.post('/check')
async def check(request):
    img = request.form.get('img')
    try:
        img = base64.b64decode(img)
    except Exception as e:
        pass
    if not img:
        return json({'msg': 'Wrong format. '})
    result = Predict.share().get_coordinate(img)
    return json({
        'msg': 'success',
        'result': result
    })


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()

    asyncio.ensure_future(Web().run())
    loop.run_forever()
