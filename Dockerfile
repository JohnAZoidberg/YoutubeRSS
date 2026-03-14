FROM python:3.12-slim
LABEL maintainer="Daniel Schäfer <daniel@danielschaefer.me>"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY youtuberss/ youtuberss/
COPY wsgi.py .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "wsgi:app"]
