FROM python:3.5.2-slim

WORKDIR /usr/src/app

RUN sh -c 'apt-get update && apt-get install -y git-core'

ADD https://api.github.com/repos/SemenovaEkaterina/expert-system/git/refs/heads/init version.json
RUN git clone -b init https://github.com/SemenovaEkaterina/expert-system.git

WORKDIR expert-system
ENV PYTHONPATH=/usr/src/app/api

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn --log-level debug --workers 4 --bind 0.0.0.0:8000 expert.wsgi
