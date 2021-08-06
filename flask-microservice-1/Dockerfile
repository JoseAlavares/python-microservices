FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . /app
RUN apt update && apt install npm -y
RUN npm i -g nodemon
#CMD nodemon --exec python main.py
