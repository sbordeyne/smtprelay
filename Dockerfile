FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./smtprelay /app/smtprelay

CMD ["python3", "-m", "smtprelay"]
