from client.zookeeper import client
from kazoo.client import KazooState
import logging
import time
import datetime

def listener(state):
    if state == KazooState.LOST:
        logging.warning('Lost connection state!')
    elif state == KazooState.CONNECTED:
        logging.warning('Connected state!')
    else:
        logging.warning('Suspended state!')

if __name__ == '__main__':
    client.start()
    client.add_listener(listener)
    time_str = time.time().__str__()
    client.create('/time', time_str.encode())
    while True:
        time.sleep(10)
        data, stat = client.get('/time')
        logging.warning('time from zookeeper value: ' + str(data, 'utf-8'))
        time_str = time.time().__str__()
        client.set('/time', time_str.encode())
