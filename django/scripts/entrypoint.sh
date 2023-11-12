#!/bin/sh

set -e

cd && cd /django/website/

uwsgi --ini /etc/django.ini