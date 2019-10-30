FROM python:3.6
WORKDIR /app

ADD socketio/ /app/socketio/
COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD ["python", "socketio/websocketio.py"]