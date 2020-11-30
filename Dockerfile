FROM python:3.7.7-slim-buster

RUN apt-get update && \
  apt-get -y install \
  --no-install-recommends \
  --allow-remove-essential \
  --allow-change-held-packages \
  --autoremove \
  build-essential \
  python-dev \
  curl && \
  rm -rf /var/lib/apt/lists

RUN pip install uwsgi

# Add web files
COPY --chown=www-data:www-data maxlevine.co.uk/ /var/src/maxlevine.co.uk/

RUN pip install /var/src/maxlevine.co.uk

EXPOSE 80
EXPOSE 9191

ENV MAX_LEVINE_DB_HOST mariadb
ENV MAX_LEVINE_DB_PASSWORD &9spEZMk3NJTRbx&mY?B
ENV MAX_LEVINE_DB_PORT 3306
ENV MAX_LEVINE_DB_USERNAME benjilevinecom
ENV MAX_LEVINE_SMTP_HOST mail.gandi.net
ENV MAX_LEVINE_SMTP_PASSWORD pMR!][3duvuQMp4dx7CY
ENV MAX_LEVINE_SMTP_PORT 465
ENV MAX_LEVINE_SMTP_USERNAME no-reply@maxlevine.co.uk
ENV FLASK_SECRET_KEY xsAshSdJNT5v7#Gv5bC&7@TVw%wrBKgZ
ENV ML_CAPTCHA_SITE_KEY 6ec438ae-13ae-4326-8dd7-393b3f977724
ENV ML_CAPTCHA_SECRET_KEY 0x7b66A87aEc5D7280b3D7FE65D8518F1AC4291650
ENV ML_CAPTCHA_VERIFY_URL https://hcaptcha.com/siteverify
ENV ML_CAPTCHA_API_URL https://hcaptcha.com/1/api.js
ENV ML_CAPTCHA_DIV_CLASS h-captcha

CMD uwsgi --http 0.0.0.0:80 --wsgi-file \
  "/var/src/maxlevine.co.uk/maxlevine" --callable app \
  --processes 1 --threads 1 --stats 0.0.0.0:9191

HEALTHCHECK --interval=10s CMD curl --fail localhost:80 || exit 1
