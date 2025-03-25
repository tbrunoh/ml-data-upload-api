FROM python:3.12-slim

WORKDIR /prep

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY .env .env
COPY scin_labels.csv scin_labels.csv
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
