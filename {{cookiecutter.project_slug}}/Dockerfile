FROM python:3.8.6-slim-buster

# Create app directory
WORKDIR /app

# Install system libraries
RUN apt update && apt install python-dev postgresql-client libxslt-dev libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev gettext -y

# Install poetry so we can use it to install all the dependencies
RUN pip install poetry

# Install dependencies
ADD pyproject.toml .
ADD poetry.lock .

# install dependencies with poetry and avoid to create a virtualenv
RUN poetry config virtualenvs.create false && poetry install

# Bundle app source
COPY . /app

# Compile translations, this should be runned with django-admin because we don't have access to the whole project setup at build time
RUN django-admin compilemessages

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
