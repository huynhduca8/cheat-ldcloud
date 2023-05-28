from index import run, accounts
from log.server import server_run, send_message, socketio
from multiprocessing.pool import ThreadPool
import time
def main():
    pool = ThreadPool(200)
    pool.map_async(run, accounts)
    while True:
        send_message(accounts)
        time.sleep(1)

if __name__ == '__main__':
    socketio.start_background_task(main)
    server_run()