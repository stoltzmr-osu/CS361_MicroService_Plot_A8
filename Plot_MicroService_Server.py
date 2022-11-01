# Reference: https://stackoverflow.com/questions/47391774/
# send-and-receive-objects-through-sockets-in-python

import socket
import pandas as pd
import pickle

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            parameters = conn.recv(1024)
            conn.send(b"Server: got parameters")
            data = b""
            while True:
                new_data = conn.recv(1024)
                if new_data == b"start_sending_data":
                    print("Server: receiving data...")
                    conn.send(b"Server: ready to accept data")
                elif "done_sending_data" in new_data.decode("utf-8"):
                    data = data + new_data
                    break
                else:
                    data = data + new_data
            data = data.decode("utf-8")
            # conn.sendall(b"got data")
            data = data.split("\n", 2)[0]  # delete last line
            print("Server: creating plot from data")
            parameters = parameters.decode("utf-8").split(",")
            df = pd.read_json(data)
            fig = df.plot(x=parameters[1], y=parameters[2], kind="line",
                          title=parameters[0])
            fig = fig.get_figure()
            data_string = pickle.dumps(fig)
            print("Server: sending figure to client")
            conn.send(data_string)
