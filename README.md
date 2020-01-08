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
cp config.toml.example config.toml
```
**3. 运行程序**
```bash
python main.py
```
用于识别文字的模型文件较大，没有放在仓库中，第一次运行会自动进行联网下载，所以可能需要等待一会才能运行起来。

## Docker 使用
```bash
docker run -d -p 8000:8000 pjialin/12306-ocr
```
启动后通过 `http://IP:8000` 进行访问

### 对接 Py12306
打开 **py12306** 目录下的 `py12306/helpers/api.py` 文件，找到 `API_FREE_CODE_QCR_API=` 的位置，并替换成当前 ocr 服务的接口地址，如：
```
API_FREE_CODE_QCR_API = 'http://127.0.0.1:8000/check/'
```

## License
[Apache License.](https://github.com/pjialin/12306-ocr/blob/master/LICENSE)

