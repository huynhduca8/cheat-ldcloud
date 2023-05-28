from flask import Flask, render_template
import socketio

async_mode = None
sio = socketio.Server(logger=True, async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
thread = None


@app.route('/')
def index():
    global thread
    return render_template('index.html')

def send_message(msg):
    sio.emit('response', msg)

def server_run():
    app.run(threaded=True)