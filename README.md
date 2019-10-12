# 12306 验证码识别服务

## 使用
需要运行在 python 3.6 以上版本

**1. 安装依赖**
```bash
git clone https://github.com/pjialin/12306-ocr

pip install -r requirements.txt
```
**2. 配置程序**
```bash
cp env.py.example env.py
```
**3. 运行程序**
```bash
python main.py
```
用于识别文字的模型文件较大，没有放在仓库中，第一次运行会自动进行联网下载，所以可能需要等待一会才能运行起来。

### 对接 Py12306
打开 **py12306** 目录下的 `py12306/helpers/api.py` 文件，找到 `API_FREE_CODE_QCR_API=` 的位置，并替换成当前 ocr 服务的接口地址，如：
```
API_FREE_CODE_QCR_API = 'http://127.0.0.1:8082/check/'
```

## Thanks
所用的模型和算法均来自 [https://github.com/zhaipro/easy12306](https://github.com/zhaipro/easy12306) 十分感谢！

## License
[Apache License.](https://github.com/pjialin/12306-ocr/blob/master/LICENSE)

