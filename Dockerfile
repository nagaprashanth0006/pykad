FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir logs configs
RUN mv config.ini configs/.
CMD [ "python3", "/app/app.py"]
