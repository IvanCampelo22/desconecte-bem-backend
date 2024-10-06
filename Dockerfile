FROM python:3.9-alpine

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev

RUN apk add --no-cache pango freetype-dev py3-pillow py3-cffi py3-brotli

ARG app_env
ENV app_env=${app_env}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app/

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install awscli

RUN chmod +x start.sh

CMD ["gunicorn","--bind",":8000","--workers","2","descbem.wsgi"]
