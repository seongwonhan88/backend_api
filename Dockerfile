FROM python:3

RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /app
ADD    ./requirements.txt   /app/
RUN    pip install -r requirements.txt

ADD    ./backend_api   /app/backend_api/
ADD    ./manage.py      /app/

CMD ["python", "manage.py", "runserver", "0:8000"]
