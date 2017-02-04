FROM ubuntu:14.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>


RUN apt-get update
RUN apt-get -y purge rsyslog
RUN apt-get -y install syslog-ng-core
ADD syslog-ng.conf /etc/syslog-ng/syslog-ng.conf

RUN rm -rf /var/apt/lib/lists/*

EXPOSE 514

CMD ["/usr/sbin/syslog-ng", "-F", "-f", "/etc/syslog-ng/syslog-ng.conf"]