FROM python:3.9.18-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NOWARNINGS yes
RUN echo "tzdata tzdata/Areas select America" | debconf-set-selections
RUN echo "tzdata tzdata/Zones/America select Sao_Paulo" | debconf-set-selections
RUN apt-get update && apt-get install -y gnupg wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable
COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . ./workdir

CMD python3 ./workdir/main.py