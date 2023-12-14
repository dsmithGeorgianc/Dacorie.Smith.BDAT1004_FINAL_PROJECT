FROM python:3.11-buster

RUN mkdir app

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/ /app/src/

#CMD ["uvicorn", "scr.main:app", "--host", "0.0.0.0", "--port", "80"]