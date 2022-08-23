FROM python:3.8.5-alpine3.12
WORKDIR /app
COPY ./src/main.py /app
COPY ./src/hdns.py /app
COPY ./src/myip.py /app
COPY ./requirements.txt /app
RUN pip install pip --upgrade && pip install -r requirements.txt
CMD ["python3", "-u", "main.py"]

