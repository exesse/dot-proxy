FROM python:3.8.2-alpine3.10

MAINTAINER Vladislav Kulbatski <kulbatski@gmail.com>

WORKDIR /usr/local/bin
COPY dot-proxy.py .

EXPOSE 53/tcp 53/udp

CMD ["python","dot-proxy.py"]
