# Pull Official Base Image
FROM python:3.10.2-alpine3.15

ENV PATH="/scripts:${PATH}"
ENV PRODUCTION=1

# Set Work Dir
WORKDIR /django/website/

# Install Psycopg2 Dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev build-base linux-headers pcre-dev

# Copy Project
COPY . .
COPY django.ini /etc/django.ini

# Install Dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /vol/django/static

RUN adduser -D david
RUN chown -R david:david /vol
RUN chmod -R 755 /vol/django
USER david

COPY ./scripts /scripts
USER root
RUN chmod +x /scripts/*

CMD ["entrypoint.sh"]