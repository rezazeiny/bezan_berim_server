#!/usr/bin/env bash


echo "python3 manage.py makemigrations"
python3 manage.py makemigrations
echo "python3 manage.py migrate"
python3 manage.py migrate