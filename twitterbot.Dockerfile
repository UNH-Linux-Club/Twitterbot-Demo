FROM debian:latest
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN pip3 install tweepy
ADD bot.py /
CMD python3 /bot.py
