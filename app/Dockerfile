FROM python:3.12

WORKDIR /app

RUN apt-get update

RUN apt install -y python3-dev pkg-config default-libmysqlclient-dev build-essential

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
