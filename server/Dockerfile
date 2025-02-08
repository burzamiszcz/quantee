FROM python:3.12-slim

WORKDIR /server

COPY ./server /server

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /uploads

EXPOSE 8000

CMD ["uvicorn", "file_upload_service:app", "--host", "0.0.0.0", "--port", "8000"]
