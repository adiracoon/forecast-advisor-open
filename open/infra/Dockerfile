FROM python:3.13-slim
WORKDIR /app
COPY open/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY open /app/open
CMD ["uvicorn", "open.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
