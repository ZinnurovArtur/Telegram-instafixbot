FROM python:3.9.13-slim-buster
# Or any preferred Python version.
WORKDIR /telegram-instafix
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD [ "python", "bot.py" ]