import socket
import struct


HOST = "192.168.206.132"
PORT = 2998


def main():
    connection = socket.socket()
    connection.connect((HOST, PORT))

    message = connection.recv(1024)
    payload = struct.unpack("<I", message)[0]

    connection.send(str(payload))
    print connection.recv(1024)

    connection.close()


if __name__ == "__main__":
    main()

