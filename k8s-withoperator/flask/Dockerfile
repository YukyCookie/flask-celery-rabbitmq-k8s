FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app", "--timeout", "600"]

EXPOSE 8080 5000