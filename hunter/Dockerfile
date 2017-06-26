FROM ubuntu:16.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD Shanghai /etc/localtime

RUN apt update
RUN apt install -y language-pack-zh-hans-base

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANGUAGE en_US:en

ADD requirements.txt /home
ADD uwsgi.ini /etc/uwsgi.ini
ADD supervisord.conf /etc/supervisord.conf

ADD ta-lib-0.4.0-src.tar.gz ta-lib.tar.gz
RUN tar -zxvf ta-lib.tar.gz
RUN rm -rf ta-lib.tar.gz 
WORKDIR /ta-lib 
RUN ./configure --prefix=/usr
RUN make
RUN make install
RUN cd ..
RUN rm -rf ta-lib

RUN apt install -y python3-dev \
                   python3-pip \
                   python-pip

RUN pip install --no-cache-dir supervisor

RUN pip3 install --no-cache-dir -r /home/requirements.txt
RUN pip3 install --no-cache-dir uwsgi


RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/*

WORKDIR /var/hunter

EXPOSE 5000 5001

CMD ["/usr/local/bin/supervisord"]
