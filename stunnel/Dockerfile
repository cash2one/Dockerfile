FROM alpine:3.3

MAINTAINER Zhou JunQian <zjqzero@gmail.com>

COPY *.template openssl.cnf /srv/stunnel/
COPY stunnel.sh /srv/

RUN set -x \
 && chmod +x /srv/stunnel.sh \
 && cat /etc/apk/repositories | sed -e 's,alpine/.*/main,alpine/edge/testing,g' >> /etc/apk/repositories \
 && addgroup -S stunnel \
 && adduser -S -G stunnel stunnel \
 && apk add --update \
        ca-certificates \
        gettext \
        libintl \
        openssl \
        stunnel \
 && cp -v /usr/bin/envsubst /usr/local/bin/ \
 && apk del --purge gettext \
 && mkdir -p /var/run/stunnel /var/log/stunnel \
 && chown -vR stunnel:stunnel /var/run/stunnel /var/log/stunnel \
 && mv -v /etc/stunnel/stunnel.conf /etc/stunnel/stunnel.conf.original

ENTRYPOINT ["/srv/stunnel.sh"]
CMD ["stunnel"]
