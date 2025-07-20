FROM python:3
ENV PYTHONUBUFFERED=1
ENV PYTHONDONTWRITEBYCODE=1

WORKDIR /app


RUN pip install --upgrade pip 
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
