FROM python:latest

COPY requirements.txt /requirements.txt

WORKDIR /app

RUN pip install -r /requirements.txt

COPY . .

RUN chmod +x ./src/main.py

CMD [ "python3", "/app/src/main.py" ]
