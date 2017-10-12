FROM debian:stretch
MAINTAINER Daniel Schäfer <daniel@danielschaefer.me>

RUN apt-get update && apt-get install -y \
    python-pip python-dev \
    apache2 libapache2-mod-wsgi

RUN rm /etc/apache2/sites-enabled/000-default.conf
COPY Youtuberss.conf /etc/apache2/sites-available/Youtuberss.conf

COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

COPY youtuberss /var/www/youtuberss
COPY run.wsgi /var/www/run.wsgi
RUN chown -R www-data:www-data /var/www
RUN a2ensite Youtuberss.conf

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
