#!/bin/bash

source /webapps/chess/bin/activate

cd /webapps/chess/lichesshub

python manage.py get_result
