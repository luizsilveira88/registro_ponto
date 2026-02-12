FROM python:3.13-slim


RUN apt-get update && \
  apt-get install -y \
  build-essential \
  libpq-dev \
  cmake \
  libgl1 \
  libglib2.0-0 \
  libsm6 \
  libxext6 \
  libxrender1 \
  libpango-1.0-0 \
  libpangoft2-1.0-0 \
  libharfbuzz-subset0 \
  gcc \
  git \
  tzdata \
  && rm -rf /var/lib/apt/lists/*

ENV TZ=America/Sao_Paulo

RUN mkdir /app 
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install debugpy watchdog