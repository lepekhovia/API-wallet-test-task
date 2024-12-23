FROM python:3.12-bullseye

ENV TZ=Europe/Saratov
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG USER=wttuser
ARG GROUP=wttgroup
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup --system --gid $GROUP_ID $GROUP && \
    adduser --system --uid $USER_ID --ingroup $GROUP $USER

RUN apt-get -qq update
RUN apt-get -qq install -y --no-install-recommends \
    curl \
    wget \
    jq \
    nano \
    netcat \
    cron \
    binutils \
    libproj-dev \
    gdal-bin \
    gettext

RUN apt-get -qq clean

RUN mkdir -p /wtt /logs /static

COPY ./requirements.txt /wtt/requirements.txt
WORKDIR /wtt

RUN chown -R $USER:$GROUP /wtt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

STOPSIGNAL SIGQUIT

COPY . /wtt
RUN chown -R $USER:$GROUP /wtt /logs

USER $USER

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=1
