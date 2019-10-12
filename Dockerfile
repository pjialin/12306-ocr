FROM python:3.6.6-slim

MAINTAINER <pjialin admin@pjialin.com>
ENV TZ Asia/Shanghai

WORKDIR /code

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python-dev libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc python-dev

COPY . .

EXPOSE 8000

CMD [ "python", "main.py"]

