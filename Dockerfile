FROM python:3.10-slim

# set workdir
WORKDIR /app

# small system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# copy and install python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# expose new app port
EXPOSE 4600

CMD ["python", "app.py"]

