# Build stage
FROM python:3.11-alpine as builder
LABEL MAINTAINER="Naga Prashanth Subraveti <nagaprashanth0006@gmail.com>"
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt


# Actual image with code
FROM python:3.11-alpine
COPY --from=builder /app /app
WORKDIR /app
