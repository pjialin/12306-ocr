import hashlib
import os
import shutil

import requests

from config import Config, Logger
from web import Web


def main():
    model_file_check();
    Web().run()


def model_file_check():
    try:
        if os.path.isfile(Config.IMAGE_MODEL_FILE):
            model_hash_verify()
            return
        Logger.info('正在下载模型文件...')
        with requests.get(Config.OCR.get('image_model_url'), stream=True) as r:
            with open(Config.IMAGE_MODEL_FILE, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                Logger.info('下载成功\n')
                model_hash_verify()
    except InvalidModelException:
        return model_file_check()


def model_hash_verify():
    """
    验证模型文件是否完整
    :return:
    """
    mode_md5 = Config.OCR.get('image_model_md5')
    if not mode_md5:
        # 跳过检测
        return
    md5 = file_md5(Config.IMAGE_MODEL_FILE)
    if md5 != mode_md5:
        os.remove(Config.IMAGE_MODEL_FILE)
        Logger.error('模型文件校验失败，正在重新下载')
        raise InvalidModelException()
    return True


def file_md5(file_path: str) -> str:
    """
    获取文件 md5
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as f:
        fmd5 = hashlib.md5()
        while True:
            buf = f.read(4096)
            if not buf:
                break
            fmd5.update(buf)
        return fmd5.hexdigest()


class InvalidModelException(Exception):
    pass


if __name__ == '__main__':
    main()
