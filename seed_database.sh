#!/bin/bash

rm db.sqlite3
rm -rf ./impactreeapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations impactreeapi
python3 manage.py migrate impactreeapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
# python3 manage.py loaddata milestones
# python3 manage.py loaddata impactplans
# python3 manage.py loaddata charities
# python3 manage.py loaddata impactplan_charities
# python3 manage.py loaddata charitycategories
