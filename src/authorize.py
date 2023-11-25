import json
import os
import socket
import re


def authorize():
    if os.path.exists('access_token.pickle'):
        os.remove('access_token.pickle')

    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(1)

    with open('config.json', 'r') as f:
        conf = json.load(f)
    print("Please open this link and authorize the app to access your strava data:")
    print(f"http://www.strava.com/oauth/authorize?client_id={conf['client_id']}"
          "&response_type=code&redirect_uri=http://localhost:8080&approval_prompt=force"
          "&scope=activity:read_all")

    while True:
        client_socket, client_address = server_socket.accept()
        message = "Authenticated!"
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        client_socket.close()

        try:
            code = re.search(r"code=.*&", data).group(0)[5:-1]
        except IndexError:
            print('authorization failed!')
            break
        conf['code'] = code
        with open('config.json', 'w') as f:
            json.dump(conf, f)
        print("Authorization successful.")
        break


if __name__ == '__main__':
    authorize()
