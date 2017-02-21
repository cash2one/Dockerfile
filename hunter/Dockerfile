
FROM ubuntu

MAINTAINER zhoujunqian <zjqzero@gmail.com>

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ADD requirements.txt /home
ADD uwsgi.ini /etc/uwsgi.ini

RUN apt update
RUN apt install -y python3-dev \
                   python3-pip

RUN pip3 install --no-cache-dir -r /home/requirements.txt
RUN pip3 install --no-cache-dir uwsgi

ADD Emquant /home/lib/Emquant
RUN ls -al /home/lib
RUN cp /home/lib/Emquant/Linux_3/libs/x64/libjson.so /usr/lib
RUN python3 /home/lib/Emquant/Linux_3/installEmQuantAPI_Ex.py

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/*



EXPOSE 5000 5001

CMD ["python3", "/var/hunter/run.py"]
