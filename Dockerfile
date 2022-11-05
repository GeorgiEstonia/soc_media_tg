FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "-b", ":8080", "main:app"]