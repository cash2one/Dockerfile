FROM alpine

MAINTAINER zhoujunqian <zjqzero@gmail.com>

RUN apk update
RUN apk add musl-dev build-base tzdata linux-headers ca-certificates
RUN apk add python3 py-pip python3-dev

WORKDIR /
COPY ta-lib-0.4.0-src.tar.gz ta-lib.tar.gz 
RUN tar -xvzf ta-lib.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

RUN rm -rf ta-lib.tar.gz && \
    rm -rf ta-lib

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

ADD requirements.txt /home

RUN pip install --no-cache-dir supervisor 
RUN pip3 install --no-cache-dir uwsgi 
RUN pip3 install --no-cache-dir -r /home/requirements.txt 

RUN apk del musl-dev build-base tzdata linux-headers

RUN rm -rf /var/cache/apk/* 
RUN rm -rf /tmp/*