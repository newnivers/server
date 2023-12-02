FROM python:3.11.4-slim

RUN apt-get -y update
RUN apt-get -y install curl

RUN pip install poetry
RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py migrate

RUN echo yes | python manage.py collectstatic


EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]