
FROM python:3.12-slim
WORKDIR /app
RUN pip install flask requests
COPY Jass-Phone-Control.py /app/
COPY Jass-Manager-V2.py /app/
EXPOSE 5000
CMD ["python", "Jass-Phone-Control.py"]
