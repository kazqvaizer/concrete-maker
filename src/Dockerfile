FROM python:3.8.6-slim-buster
LABEL maintainer="kazqvaizer@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV _UWSGI_VERSION 2.0.19.1

EXPOSE 8000

RUN apt-get update \
    && apt-get --no-install-recommends install -y gettext locales-all wget build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
    && tar zxvf uwsgi-*.tar.gz \
    && UWSGI_BIN_NAME=/usr/local/bin/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
    && rm -Rf uwsgi-*

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /srv
ADD . /srv/

ENV ON_BUILD_ENV_FILE=.env.ci

RUN ENV_FILE=$ON_BUILD_ENV_FILE ./manage.py compilemessages
RUN ENV_FILE=$ON_BUILD_ENV_FILE ./manage.py collectstatic --noinput

HEALTHCHECK --interval=15s --timeout=15s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://localhost:8000/api/v1/healthchecks/db/ --header "Host: concrete.kazqvaizer.xyz" || exit 1

CMD uwsgi --http :8000 --module app.wsgi --workers 2 --threads 2 --harakiri 40 --max-requests 500 --static-map /static/=/static/
