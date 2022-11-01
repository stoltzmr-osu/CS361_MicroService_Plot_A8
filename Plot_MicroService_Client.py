import pandas as pd
import socket
import pickle
from datetime import datetime

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

user_input = ""

while user_input.lower() != "exit":
    user_input = input("Press enter to continue or type exit: ")
    title = input("Title: ")
    x_axis = input("X axis: ")
    y_axis = input("Y axis: ")
    parameters = title + "," + x_axis + "," + y_axis
    csv_file = input("CSV file: ")
    df = pd.read_csv(csv_file)  # Data_Baseball\Aaron_Nola.csv
    df = df.to_json()
    print()
    if user_input.lower() != "exit":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(bytes(parameters, encoding="utf-8"))
            print(s.recv(1024))
            s.send(b"start_sending_data")
            print(s.recv(1024))
            print("Client: sending data")
            s.sendall(bytes(df, encoding="utf-8"))
            s.send(b"\ndone_sending_data")
            data = s.recv(200000)
            fig = pickle.loads(data)
            dt = datetime.now()
            dt = dt.strftime("%m-%d-%Y_%H%M%S")
            save_name = title.replace("/", "") + "_" + dt + ".png"
            save_name = save_name.replace(" ", "")
            fig.savefig("output/" + save_name)
            print("Client: figure from server saved as output/" + save_name)

        print("")
