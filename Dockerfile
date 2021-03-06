FROM python:3.8.2-alpine3.10

MAINTAINER Vladislav Kulbatski <kulbatski@gmail.com>

WORKDIR /usr/local/bin
COPY dot_proxy.py .

EXPOSE 53/tcp
EXPOSE 53/udp

CMD ["python","dot_proxy.py"]
