FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x run_app.sh
ENTRYPOINT [ "/app/run_app.sh" ]
