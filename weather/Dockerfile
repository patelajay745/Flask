# ------------------- Stage 1: Build Stage ------------------------------
FROM python:3.8 AS builder

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# ------------------- Stage 2: Final Stage ------------------------------

FROM python:3.8-slim

WORKDIR /app

RUN apt-get update 

COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

COPY --from=builder /app /app

EXPOSE 5000

CMD ["python", "app.py"]
