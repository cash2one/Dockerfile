
FROM ubuntu

MAINTAINER zhoujunqian <zjqzero@gmail.com>

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ADD requirements.txt /home

RUN apt update
RUN apt install -y python3-dev \
                   python3-pip

RUN pip3 install --no-cache-dir -r /home/requirements.txt
RUN pip3 install --no-cache-dir uwsgi, gunicorn

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/*

EXPOSE 5000 5001

CMD ["/var/hunter/run.sh"]