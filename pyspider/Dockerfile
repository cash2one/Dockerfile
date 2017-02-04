FROM cmfatih/phantomjs 

MAINTAINER binux <zjqzero@gmail.com> 
# install python 

RUN apt-get update && \
        apt-get install -y python python-pip && \
        apt-get install -y libcurl4-openssl-dev libxml2-dev libxslt1-dev libpq-dev python-dev

# install requirements 
RUN pip install -U pip setuptools
RUN pip install --no-cache-dir --egg http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.3.zip#md5=710479afc4f7895207c8f96f91eb5385

ADD requirements.txt /opt/pyspider/requirements.txt

RUN pip install --no-cache-dir -r /opt/pyspider/requirements.txt

# clean
RUN apt-get purge -y libcurl4-openssl-dev libxml2-dev libxslt1-dev libpq-dev python-dev
RUN rm -rf /var/lib/apt/lists/*

# add all repo ADD ./ /opt/pyspider
# run test WORKDIR /opt/pyspider

VOLUME ["/opt/pyspider"]

ENTRYPOINT ["pyspider"]

EXPOSE 5000 23333 24444 25555