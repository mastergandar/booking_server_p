###########
# BUILDER #
###########
FROM python:3.9-slim-bullseye

LABEL maintainer="Vladimir Kolganov <titanitewow@gmail.com>"

RUN apt-get update -y && apt install -y netcat ffmpeg python3.9-dev

# create the appropriate directories
ENV HOME=/usr/src/app
WORKDIR $HOME

ARG INSTALL_DEV_REQUIREMENTS="false"
# change it in production via build command
ARG DJANGO_SECRET_KEY="DJANGO_SECRET_KEY"
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    && if [ "$INSTALL_DEV_REQUIREMENTS" = "false" ]; then \
            pipenv install --system --deploy; \
        else \
            pipenv install --dev --system --deploy; \
        fi

# copy project
COPY . $APP_HOME

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH static

# URL under which media (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV MEDIA_URL /media
# Absolute path in where the media files wil be
ENV MEDIA_PATH media

RUN python manage.py collectstatic --noinput

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]