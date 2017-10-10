FROM nginx:latest

ADD https://api.github.com/repos/SemenovaEkaterina/expert-system/git/refs/heads/init version.json
RUN git clone -b init https://github.com/SemenovaEkaterina/expert-system.git /var/www/html
