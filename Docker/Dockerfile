FROM ubuntu:latest

LABEL maintainer="Ron Haber"

RUN apt-get update && apt-get install -y python-dev python3-pip
RUN apt-get install -y git cron

COPY cron /etc/cron.d/cron
COPY api_keys.sh /bin/api_keys.sh

RUN chmod +x /bin/api_keys.sh

ARG token=0

RUN git clone "https://haberrj:${token}@github.com/haberrj/dockerized_binance.git"

RUN mkdir /Artifacts

WORKDIR /dockerized_binance/

RUN git remote set-url origin "https://haberrj:${token}@github.com/haberrj/dockerized_binance.git"
RUN pip3 install -r requirements.txt

RUN chmod +x /dockerized_binance/Crontabs/allow_all.sh
RUN chmod 0644 /etc/cron.d/cron

RUN crontab /etc/cron.d/cron
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log

ENTRYPOINT [ "/bin/api_keys.sh" ]