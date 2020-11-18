FROM ubuntu:latest
# MAINTAINER Ron Haber

RUN apt-get update && apt-get install -y python3 python3-pip python-dev
RUN apt-get install -y git

COPY ./Tokens/access_token /bin/
ARG TOK=
RUN TOKEN=`cat bin/access_token`
RUN echo $TOKEN

# # RUN git config --global url."https://{$TOKEN}@github.com/".insteadOf "https://github.com/" files to docker
# RUN git clone "https://{$TOKEN}:github.com/haberrj/CryptoCurrency.git"

# RUN rm /bin/access_token \
#     TOKEN = ""

# WORKDIR /CryptoCurrency/

# RUN pip3 install requirements.txt

# # Some code here will run the app or setup the cronjob
# # will need to replace the cronjob document

# ENTRYPOINT [ "bash" ]
# CMD [ "/Crontabs/mock_execution_binance.sh" ]