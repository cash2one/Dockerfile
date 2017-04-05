FROM ubuntu:16.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD ./bin64 /ths_lib/bin64
RUN ldd /ths_lib/bin64/libShellExport.so
RUN ldd /ths_lib/bin64/libFTDataInterface.so
RUN apt update
RUN apt install -y python3 \
                   python3-dev \
                   python3-pip
RUN python3 /ths_lib/bin64/installiFinDPy.py /ths_lib

CMD python3 /var/app/run.py
