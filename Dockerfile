FROM alpine:3.6

ENV S6_OVERLAY_VERSION=v1.21.4.0
RUN apk add --update --no-cache --virtual=deps bind-tools curl libcap && \
    curl -sSL https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-amd64.tar.gz \
    | tar xfz - -C / && \
    apk del deps

ENV LANG=en_US.utf8 \
    MUSL_LOCPATH=en_US.utf8

RUN apk upgrade --update --no-cache && \
    apk add --update --no-cache \
        postgresql-dev  \
        nginx  \
        uwsgi-python3  \
        python3

RUN apk --no-cache add --virtual=build_deps gcc \
        libffi-dev \
        musl-dev \
        python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools pipenv && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

ADD ./Pipfile /opt/app/backend/
ADD ./Pipfile.lock /opt/app/backend/

RUN cd /opt/app/backend && pipenv install --system --verbose && \
    apk del build_deps

ADD rootfs /
ADD backend /opt/app/backend
