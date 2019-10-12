import asyncio
import os
import shutil

import requests

from config import Config, Logger
from web import Web


def main():
    model_file_check();
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(Web().run())
    loop.run_forever()


def model_file_check():
    if os.path.isfile(Config.IMAGE_MODEL_FILE):
        return
    Logger.info('正在下载模型文件...')
    with requests.get(Config.OCR.get('image_model_url'), stream=True) as r:
        with open(Config.IMAGE_MODEL_FILE, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            Logger.info('下载成功\n')


if __name__ == '__main__':
    main()
