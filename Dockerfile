FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 7700 ## Can be overridden from kuebernetes api objects.
CMD [ "python3", "/app/app.py"]
