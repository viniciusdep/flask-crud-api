# syntax=docker/dockerfile:1
FROM python
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --src /usr/local/src
COPY . . 
EXPOSE 5000
CMD [ "python3", "clientes.py"]