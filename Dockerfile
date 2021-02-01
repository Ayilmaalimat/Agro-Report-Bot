FROM python:3.9.1

RUN mkdir -p C:/Users/Administrator/Desktop/3/

WORKDIR C:/Users/Administrator/Desktop/3/
COPY . C:/Users/Administrator/Desktop/3/

RUN pip install -r requirements.txt

CMD ["python", "server.py"]