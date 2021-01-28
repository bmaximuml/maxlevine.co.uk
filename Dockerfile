FROM python:3.9-alpine

ARG USER=maxlevine
ARG WORKDIR=/run/

RUN set -aeux; \
    apk add --update --no-cache curl ; \
    adduser \
        -H \
        -D \
        ${USER} && \
    export PATH=${WORKDIR}${USER}/.local/bin:${PATH}

WORKDIR ${WORKDIR}${USER}

# Add web files
COPY src/ ./

RUN pip install gunicorn .

EXPOSE 80
# EXPOSE 9191

CMD gunicorn -w 1 -b 0.0.0.0:80 maxlevine:app

HEALTHCHECK --interval=10s CMD curl --fail localhost:80 || exit 1
