FROM python:3.9.5-alpine
WORKDIR /src
RUN apk --no-cache add build-base
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
