from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")


@app.route('/')
def index():
    global thread
    return render_template('index.html')

def send_message(msg):
    socketio.emit('response', msg)

def server_run():
    socketio.run(app)