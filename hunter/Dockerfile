
FROM python:3-alpine

MAINTAINER zhoujunqian <zjqzero@gmail.com>


RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ADD requirements.txt /home
RUN apk update
RUN apk add --no-cache supervisor \
                       py-gunicorn

RUN pip install --no-cache-dir -r /home/requirements.txt
RUN pip install --no-cache-dir uwsgi
RUN apk del python-dev libffi-dev build-base musl-dev linux-headers
RUN rm -rf /var/cache/apk/* 
RUN rm -rf /tmp/*

EXPOSE 5000 5001


