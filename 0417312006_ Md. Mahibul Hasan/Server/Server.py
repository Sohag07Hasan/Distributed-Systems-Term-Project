#!/usr/bin/python3
import socket, math, json, time

#handle socket
def launch_socket():
    #create a socket object
    serversocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    host = socket.gethostname()  # get local machine name
    port = 9999
    serversocket.bind((host, port)) # bind to the port
    serversocket.listen(8) # queue up to 8 requests

    server_info = read_server() #read info to send to client
    info = server_info['info']
    series = server_info['series']

    client_number = 0;
    start_time = False
    end_time = False
    while True:

        if client_number == 0:
            start_time = time.time()

        # establish a connection
        clientsocket, addr = serversocket.accept()
        print("Got a connection from %s" % str(addr))
        print("Clinet Number %s" % str(client_number))
        message = clientsocket.recv(1024)
        message = message.decode('ascii')
        message = json.loads(message)
        if message['status'] == 'retry':
            if client_number < len(series):
                message = { 'status': 'ok', 'info': info, 'series': series[client_number] }
                message = json.dumps(message)
            else:
                message = {'status': 'stop', 'message': 'Number allocation finished'}
                message = json.dumps(msg)
        elif message['status'] == 'solved':
            print(message['key'])
            end_time = time.time()
            time_required = end_time - start_time
            print ("time Required (ms) %s", time_required)
            line = [key, start_time, end_time, time_required]
            write_file(line) #writing file

        else:
            message = {'status': 'stop', 'message': 'retry not send by the client'}

        client_number += 1
        clientsocket.sendall(message.encode('ascii'))
        clientsocket.close()


#reading server information
#process series return to socket processing functions
def read_server():
    # server variables to send to client
    input = read_file()
    info = {
        'T': input[0].strip(),
        'HT': input[1].strip(),
    }
    keys = {
        'start': int(input[2].strip()), # converting string to integer
        'end': int(input[3].strip()),
        'interval': int(input[4].strip()),
    }

    series = []
    start, end, interval = keys['start'], keys['end'], keys['interval']

    while start < end:
        new_start = start + interval
        if new_start < end:
            series.append([start, new_start])
            start += interval + 1
        else:
            series.append([start, end])
            break;

    return {'info': info, 'series': series}


#read server file
def read_file():
    try:
        fh = open("server_input.txt", "r")
        info = fh.readlines()[1]
        fh.close()
        return info.split(",")
    except:
        print("failed ro read server_input.txt")
        raise

def write_file(line):
    try:
        fh = open("server_output.txt", "r")
        lines = ["key, start_timestamp, end_timestamp, duration_seconds"]
        line = ", ".join(line)
        lines.append(line)
        fh.writelines(lines)
        fh.close()
    except:
        print("failed to write server_output.txt")
        raise


#launch the module
if __name__ == '__main__':
    launch_socket()