# coding: utf-8
import cv2
import tensorflow as tf
import numpy as np
from keras import models

from config import Logger, Config

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class ShareInstance():
    __session = None

    @classmethod
    def share(cls, **kwargs):
        if not cls.__session:
            cls.__session = cls(**kwargs)
        return cls.__session


class Predict(ShareInstance):
    def __init__(self):
        # 识别文字
        self.model = models.load_model(Config.TEXT_MODEL_FILE, compile=False)

        with open(Config.TEXTS_FILE, encoding='utf-8') as f:
            self.texts = [text.rstrip('\n') for text in f]

        # 加载图片分类器
        self.code_model = models.load_model(Config.IMAGE_MODEL_FILE, compile=False)

    def get_text(self, img, offset=0):
        text = img[3:22, 120 + offset:177 + offset]
        text = cv2.cvtColor(text, cv2.COLOR_BGR2GRAY)
        text = text / 255.0
        h, w = text.shape
        text.shape = (1, h, w, 1)
        return text

    def get_coordinate(self, img_str):
        # 储存最终坐标结果
        result = ''

        try:
            # 读取并预处理验证码
            img = cv2.imdecode(np.fromstring(img_str, np.uint8), cv2.IMREAD_COLOR)
            text = self.get_text(img)
            images = np.array(list(self._get_imgs(img)))
            images = self.preprocess_input(images)

            label = self.model.predict(text)
            label = label.argmax()
            text = self.texts[label]

            # list放文字
            titles = [text]

            position = []

            # 获取下一个词
            # 根据第一个词的长度来定位第二个词的位置
            if len(text) == 1:
                offset = 27
            elif len(text) == 2:
                offset = 47
            else:
                offset = 60
            text2 = self.get_text(img, offset=offset)
            if text2.mean() < 0.95:
                label = self.model.predict(text2)
                label = label.argmax()
                text2 = self.texts[label]
                titles.append(text2)

            labels = self.code_model.predict(images)
            labels = labels.argmax(axis=1)

            for pos, label in enumerate(labels):
                if self.texts[label] in titles:
                    position.append(pos + 1)

            # 没有识别到结果
            if len(position) == 0:
                return result
            result = position
            Logger.info('识别结果: %s' % result)
        except:
            pass
        return result

    def preprocess_input(self, x):
        x = x.astype('float32')
        # 我是用cv2来读取的图片，其已经是BGR格式了
        mean = [103.939, 116.779, 123.68]
        x -= mean
        return x

    def _get_imgs(self, img):
        interval = 5
        length = 67
        for x in range(40, img.shape[0] - length, interval + length):
            for y in range(interval, img.shape[1] - length, interval + length):
                yield img[x:x + length, y:y + length]


if __name__ == '__main__':
    for i in range(10):
        with open('test.jpg', 'r') as f:
            print(Predict.share().get_coordinate(f.buffer.read()))
