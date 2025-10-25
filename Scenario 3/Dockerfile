FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV MODEL_PATH=/app/model.pkl

# expose app port
EXPOSE 8000

CMD ["gunicorn", "--bind",",0.0.0.0:8000", "app:app", "--workers", "3"]
