FROM python:3.8.1-alpine3.11

ARG ENCRYPT_KEY

WORKDIR /home/telegram-stickers
RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc postgresql-dev musl-dev zlib-dev jpeg-dev make gnupg \
    && pip3 install --upgrade pip
COPY ../../requirements.txt /home/telegram-stickers/
RUN pip3 install -r requirements.txt
COPY deploy/stage/telegram-stickers-stage.json.gpg telegram_stickers/ /home/telegram-stickers/
RUN gpg --quiet --batch --yes --decrypt --passphrase="$ENCRYPT_KEY" \
    --output telegram-stickers-stage.json telegram-stickers-stage.json.gpg
CMD uvicorn telegram_stickers.asgi:application --host 0.0.0.0 --port 80 --workers 4
EXPOSE 80
