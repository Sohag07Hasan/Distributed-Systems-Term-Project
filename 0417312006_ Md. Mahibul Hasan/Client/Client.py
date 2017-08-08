#!/usr/bin/python3           # This is client.py file

import socket, json, sys, gevent
from hmac_md5 import hmac_md5

def launch_client():
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()  # get local machine name
    port = 9999
    s.connect((host, port)) # connection to hostname on the port.
    message = {'status': 'retry'}


    while True:
        send_message(s, message)
        received_msg = receive_message(s)

        if received_msg['status'] == 'ok':
            process_result = process_encryption(received_msg['series'], received_msg['info'])
            print(process_result)
            if process_result['status'] == 'done':
                message = {'status': 'solved', 'key': process_result['key']}
                send_message(s, message)
                print("Solved: key is %s", process_result['key'])
                break

        else:
            print ("Server message: %s", received_msg['message'] )
            break

    s.close()

#send socket request
#@s = socket object, @message = message to be sent to server
def send_message(s = False, message = False):
    message = json.dumps(message)
    try:
        s.send(message.encode('ascii'))
    except:
        raise

#receive message from server
def receive_message(s = False, size = 1024):
    msg = s.recv(size)
    msg = msg.decode('ascii')
    msg = json.loads(msg)
    return msg


#process encryption and match with encrypted message
def process_encryption(series, info):
    start = int(series[0])
    end = int(series[1])
    result = {'status': 'retry'}
    while start <= end:
        encypted = hmac_md5(start, info['T'])
        print(encypted)
        if encypted.upper() == info['HT']:
            result = {'key': start, 'status': 'done'}
            break

        start += 1
    return result


if __name__ == "__main__":
    launch_client()