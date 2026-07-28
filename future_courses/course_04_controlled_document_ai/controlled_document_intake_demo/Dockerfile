FROM python:3.12.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY src ./src
COPY static ./static
COPY fixtures ./fixtures

RUN useradd --create-home --uid 10001 appuser
USER appuser

CMD ["sh", "-c", "uvicorn controlled_intake.main:app --app-dir src --host 0.0.0.0 --port ${PORT} --no-access-log"]
