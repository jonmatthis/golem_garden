FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "localhost", "--port", "8000"]
