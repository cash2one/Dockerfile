FROM ubuntu:16.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD Shanghai /etc/localtime
ADD uwsgi.ini /etc/uwsgi.ini
ADD supervisord.conf /etc/supervisord.conf

ADD ./bin64 /ths_lib/bin64
RUN ldd /ths_lib/bin64/libShellExport.so
RUN ldd /ths_lib/bin64/libFTDataInterface.so
RUN apt update
RUN apt install -y python3 \
                   python3-dev \
                   python3-pip \
                   python-pip \
                   libidn11

RUN pip install --no-cache-dir supervisor
RUN pip3 install --no-cache-dir uwsgi

RUN python3 /ths_lib/bin64/installiFinDPy.py /ths_lib

CMD ["/usr/local/bin/supervisord"]
