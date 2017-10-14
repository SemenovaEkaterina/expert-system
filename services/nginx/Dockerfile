FROM nginx:latest

RUN sh -c 'apt-get update && apt-get install -y git'

ADD https://api.github.com/repos/SemenovaEkaterina/expert-system/git/refs/heads/master version.json
RUN git clone -b master https://github.com/SemenovaEkaterina/expert-system.git /var/www/html
