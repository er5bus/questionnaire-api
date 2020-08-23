FROM python:3.7

LABEL MAINTAINER="Rami sfari <rami2sfari@gmail.com>"

COPY ./requirements.txt /requirements.txt

# Install Dependencies
RUN ["pip", "install", "-r", "/requirements.txt"]

# Copy files
COPY ./survey /survey
WORKDIR /survey


EXPOSE 5000 9191

# Create New user & group
RUN groupadd -r uswgi && useradd -r -g uswgi uswgi
USER uswgi


COPY ./entrypoint.sh /entrypoint.sh

# Runtime configuration
ENTRYPOINT ["/entrypoint.sh"]
