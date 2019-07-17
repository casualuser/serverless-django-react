#!/bin/sh
sls wsgi manage local -c "makemigrations authentication"
sls wsgi manage local -c "migrate authentication"
