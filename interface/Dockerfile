FROM python:3.11.2-buster as base 
LABEL Sobolev Andrey
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install bash -y && \
    apt-get upgrade -y && \
    apt-get install -y \
    gcc && apt-get install -y \
    apt-utils libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev libjpeg-dev libfreetype6-dev python-dev libpq-dev python-dev libxml2-dev libxslt-dev postgresql-client git && \
    pip3 install -U pip setuptools && apt-get install python3-dev -y && apt-get install libev-dev -y && pip3 install --upgrade pip

RUN echo "alias rm='rm -i'" >> ~/.bashrc && \
    echo "alias cp='cp -i'" >> ~/.bashrc && \
    echo "alias mv='mv -i'" >> ~/.bashrc && \
    echo "alias ls='ls --color=auto'" >> ~/.bashrc && \
    echo "alias ll='ls -la'" >> ~/.bashrc && \
    echo "alias grep='grep --color=auto'" >> ~/.bashrc && \
    echo "alias egrep='egrep --color=auto'" >> ~/.bashrc && \
    echo "alias fgrep='fgrep --color=auto'" >> ~/.bashrc && \
    echo "alias ports='netstat -tulanp'" >> ~/.bashrc && \
    echo "alias df='df -H'" >> ~/.bashrc && \
    echo "alias du='du -ch'" >> ~/.bashrc

WORKDIR /interface/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

FROM base as prod
CMD gunicorn --bind 0.0.0.0:12345 --threads 2 --workers 5 --reload wsgi

FROM base as dev
ENTRYPOINT ["tail", "-f", "/dev/null"]
# CMD python manage.py runserver 0.0.0.0:12345

FROM base as test
CMD pytest