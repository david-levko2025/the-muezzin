FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/

WORKDIR /app 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

FROM base AS metadata-service
COPY ./share ./share/
COPY metadata/ ./metadata
CMD ["python", "-m", "metadata.main" ]

FROM base AS mongo-loader
COPY ./share ./share/
COPY mongo/ ./mongo
CMD ["python", "-m", "mongo.main" ]

FROM base AS information-processing
COPY ./share ./share/
COPY process_info/ ./process_info
CMD ["python", "-m", "process_info.main" ]