FROM python:3.7-slim

WORKDIR /app

COPY distrib .

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "distrib.wsgi:application", "--bind", "0:8000" ]
