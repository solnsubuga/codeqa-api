# Q & A application API

An application that allows users to ask questions and receive answers from other users.

[![Build Status](https://travis-ci.com/solnsubuga/codeqa-api.svg?branch=master)](https://travis-ci.com/solnsubuga/codeqa-api) [![Coverage Status](https://coveralls.io/repos/github/solnsubuga/codeqa-api/badge.svg?branch=master)](https://coveralls.io/github/solnsubuga/codeqa-api?branch=master)

## Dependancies

- [python 3.6](https://www.python.org/downloads/release/python-360/)
- [django](https://www.djangoproject.com/)
- [django rest framework](https://www.django-rest-framework.org/)

## Set Up

In order to run the API Application

1.  Clone this Repository to your development machine

2.  Create a virtual environment in a terminal shell `virtualenv env` and Install the dependencies `pip install -r requirements.txt`

3.  Setup the postgres and add the database configs to `settings\dev.py`
    ```
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'codeqa',
                'HOST': 'localhost',
                'USER': 'postgres',
                'PASSWORD': '',
                'PORT': '5432'
            }
        }
    ```
4.  Run the migrations using the dev settings file: `./manage.py migrate --settings=codeqaapi.settings.dev`

5.  Run the application by running commands `./manage.py runserver --settings=codeqaapi.settings.dev`

## API End points

| EndPoint                                             | Method | Description                  |
| ---------------------------------------------------- | ------ | ---------------------------- |
| `/auth/signup`                                       | POST   | Register a user              |
| `/auth/signin`                                       | POST   | Login a user                 |
| `/api/v1/questions/`                                 | GET    | Get questions                |
| `/api/v1/questions/`                                 | POST   | Post a question              |
| `/api/v1/question/<question_id>/`                    | GET    | Get a specific question      |
| `/api/v1/question/<question_id>/answers/`            | GET    | Get answers to a question    |
| `/api/v1/question/<question_id>/answers/`            | POST   | Post an answer to a question |
| `/api/v1/question/<question_id>/answers/<answer_id>` | PUT    | Edit an answer               |

## License

The project is licensed under MIT License.
