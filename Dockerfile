FROM python:3.13

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Ниже команда только для docker compose
RUN chmod a+x /booking/docker/*.sh

# Ниже комнда если надо запустить только Dockerfile, раскоментируйте строку ниже и закомментируйте строку выше
#CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

