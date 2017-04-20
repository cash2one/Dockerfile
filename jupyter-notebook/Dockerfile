FROM ubuntu:16.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD Shanghai /etc/localtime

RUN apt update
RUN apt install -y language-pack-zh-hans-base

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANGUAGE en_US:en

ADD start.sh /start.sh
ADD requirements3.txt /requirements3.txt
ADD key.pem /key.pem
COPY ta-lib-0.4.0-src.tar.gz ta-lib.tar.gz

# RUN apt-get install -y python python-dev python-pip
RUN apt install -y python3 python3-dev python3-pip
RUN pip3 install --no-cache-dir jupyter ipython
# RUN python2 -m pip install --no-cache-dir ipykernel
# RUN python2 -m ipykernel install --user

RUN tar -zxvf ta-lib.tar.gz
RUN rm -rf ta-lib.tar.gz 
WORKDIR /ta-lib 
RUN ./configure --prefix=/usr
RUN make
RUN make install
RUN cd ..
RUN rm -rf ta-lib

WORKDIR /
RUN pip3 install --no-cache-dir -r requirements3.txt

RUN rm -rf /var/lib/apt/lists/*

ADD SimSun.ttf /usr/lib/python3/dist-packages/matplotlib/mpl-data/fonts/ttf
ADD matplotlibrc /usr/lib/python3/dist-packages/matplotlib/mpl-data/matplotlibrc

VOLUME /notebooks
WORKDIR /notebooks

EXPOSE 8888



CMD ["/start.sh"]
