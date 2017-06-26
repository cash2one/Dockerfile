
FROM ubuntu

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD Shanghai /etc/localtime
ADD requirements.txt /home
ADD uwsgi.ini /etc/uwsgi.ini
ADD supervisord.conf /etc/supervisord.conf

RUN apt update
RUN apt install -y python3-dev \
                   python3-pip \
                   python-pip

RUN pip install --no-cache-dir supervisor

RUN pip3 install --no-cache-dir -r /home/requirements.txt
RUN pip3 install --no-cache-dir uwsgi

ADD Emquant /home/lib/Emquant
RUN ls -al /home/lib
RUN cp /home/lib/Emquant/Linux_3/libs/x64/libjson.so /usr/lib
RUN python3 /home/lib/Emquant/Linux_3/installEmQuantAPI_Ex.py

ADD ta-lib-0.4.0-src.tar.gz ta-lib.tar.gz
RUN tar -zxvf ta-lib.tar.gz
RUN rm -rf ta-lib.tar.gz 
WORKDIR /ta-lib 
RUN ./configure --prefix=/usr
RUN make
RUN make install
RUN cd ..
RUN rm -rf ta-lib

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/*

WORKDIR /var/hunter

EXPOSE 5000 5001

CMD ["/usr/local/bin/supervisord"]
