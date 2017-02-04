FROM alpine:3.4

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD requirements.txt /home
RUN apk update
RUN apk add py-pip \
            python-dev \
            libffi-dev \
            musl-dev \
            supervisor \
            build-base \
            linux-headers \
            py-gunicorn

RUN pip install --no-cache-dir -r /home/requirements.txt
RUN pip install --no-cache-dir uwsgi
RUN apk del python-dev libffi-dev build-base musl-dev linux-headers
RUN rm -rf /var/cache/apk/* 
RUN rm -rf /tmp/*



