FROM ubuntu:18.04

LABEL maintainer="Ron Haber"

RUN apt-get update && apt-get install -y python3 python3-pip python-dev
RUN apt-get install -y git

COPY ./Tokens/access_token /bin/
ARG token=

RUN git clone "https://haberrj:${token}@github.com/haberrj/dockerized_binance.git"

WORKDIR /dockerized_binance/

RUN git remote set-url origin "https://haberrj:${token}@github.com/haberrj/dockerized_binance.git"
RUN pip3 install -r requirements.txt

# # Some code here will run the app or setup the cronjob
# # will need to replace the cronjob document

# ENTRYPOINT [ "bash" ]
# CMD [ "/Crontabs/mock_execution_binance.sh" ]git a