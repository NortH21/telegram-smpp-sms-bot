FROM python:3.7-alpine

WORKDIR /app

COPY ./lib lib
COPY ./requirements.txt requirements.txt
COPY ./smsbot.py smsbot.py

RUN apk add --no-cache git && pip install -r requirements.txt

USER 1000

CMD [ "python", "./smsbot.py" ]
