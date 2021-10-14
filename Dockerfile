FROM python:3.8

WORKDIR /app

COPY requirements-dev.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["./docker/entrypoint.sh"]
