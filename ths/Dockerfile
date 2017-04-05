FROM ubuntu:16.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD ./bin64 /ths_lib
RUN ls /ths_lib
RUN apt update
RUN apt install -y python3 \
                   python3-dev \
                   python3-pip

CMD python3 /var/app/run.py
