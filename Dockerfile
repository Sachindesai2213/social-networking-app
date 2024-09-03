FROM python:3.11

WORKDIR /social-media-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]