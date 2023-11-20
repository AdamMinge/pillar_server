FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"
ENV PYTHONPATH="/app:${PATH}"

RUN pip install --upgrade pip
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers

COPY ./requirements/requirements.txt requirements.txt
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt && rm requirements.txt; fi
COPY ./requirements/developments.txt developments.txt
RUN if [ -f "developments.txt" ]; then pip install --no-cache-dir -r developments.txt && rm developments.txt; fi

RUN mkdir /app
COPY ./app /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user