FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install flask

EXPOSE 5500

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["python3", "main.py"]