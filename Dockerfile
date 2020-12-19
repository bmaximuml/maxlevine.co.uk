FROM python:3.9-alpine

RUN apk add --update --no-cache curl

RUN pip install gunicorn

WORKDIR /var/src/maxlevine.co.uk

# Add web files
COPY ./ ./

RUN pip install .

EXPOSE 80
EXPOSE 9191

CMD gunicorn -w 1 -b 0.0.0.0:80 maxlevine:app

HEALTHCHECK --interval=10s CMD curl --fail localhost:80 || exit 1
