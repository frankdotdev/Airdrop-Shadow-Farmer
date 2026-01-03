FROM python:3.12-slim

WORKDIR /app
COPY . /app
RUN pip install poetry
RUN poetry install --no-dev
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]