FROM python:3.11.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY . /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --default-timeout=200 -r requirements.txt

EXPOSE 5001

ENV DATABASE_URL="sqlite:///recipe.db"

CMD ["python", "main.py"]