FROM python:3.6

LABEL MAINTAINER="Rami sfari <rami2sfari@gmail.com>"

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
