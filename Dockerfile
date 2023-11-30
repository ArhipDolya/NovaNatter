FROM python:3.10

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc musl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get remove -y gcc musl-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["sh", "-c", "find . -name '*.py' | entr -r uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 2"]
