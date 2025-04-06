# Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl wget gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm-dev libasound2 \
    libpangocairo-1.0-0 libxshmfence1 libglu1-mesa \
    fonts-liberation libappindicator3-1 xdg-utils && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install playwright && playwright install --with-deps

COPY . .

EXPOSE 10000

CMD ["gunicorn"  , "-b", "0.0.0.0:10000", "main:app"]