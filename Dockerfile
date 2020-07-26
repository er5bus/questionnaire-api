FROM python:3.7

LABEL MAINTAINER="Rami sfari <rami2sfari@gmail.com>"

# uwsgi Dependencies
#RUN apt install python3-dev postgresql-dev build-base pcre-dev

COPY ./entrypoint.sh ./requirements.txt /

# Install Dependencies
RUN ["pip", "install", "-r", "/requirements.txt"]

# Create New user & group
RUN groupadd -r uswgi && useradd -r -g uswgi uswgi
USER uswgi

# Copy files
COPY ./survey /survey
WORKDIR /survey

EXPOSE 5000 9191

# Runtime configuration
ENTRYPOINT ["/entrypoint.sh"]
