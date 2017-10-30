# lichesshub
A platform for organising chess tournaments that ride on lichess.org

Getting Started
===============

First create the virtual environment and activate it. You may need virtualenv wrapper.

`mkvirtualenv lichesshub`

`workon lichesshub`

Then clone the repository

`git clone https://github.com/AfricaChess/lichesshub`

Go into the repo

`cd lichesshub`

Install the dependencies

`pip install -r requirements.txt`

Migrate

`python manage.py migrate`

Create a super user

`python manage.py createsuperuser`

Run development server

`python manage.py runserver`

Navigate to http://localhost:8000/ to see your site
