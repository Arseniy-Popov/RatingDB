FROM python:3.8
WORKDIR /app
COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . ./
CMD gunicorn "ratingdb.wsgi:application" --bind 0.0.0.0:8000 
