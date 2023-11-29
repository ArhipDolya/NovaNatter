FROM python:3.10-alpine

WORKDIR /app

COPY . .

COPY requirements.txt .

# Install build dependencies and PostgreSQL development libraries
RUN apk --no-cache add --virtual .build-deps postgresql-dev gcc musl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del .build-deps  # Remove build dependencies after installation

EXPOSE 8000

CMD ["sh", "-c", "find . -name '*.py' | entr -r uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 2"]
