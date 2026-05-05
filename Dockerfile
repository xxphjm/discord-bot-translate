FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY help.json .

ENV DISCORD_TOKEN=""
ENV MAKE_API_KEY=""
ENV WEBHOOK_URL=""

CMD ["python", "bot.py"]
