import socket
import re
from time import sleep
import struct


def main():
    connection = socket.socket()
    connection.connect(("192.168.206.132", 2997))

    sleep(1)  # Wait 1 second before recieving. Generating random numbers takes time for the server.

    message = connection.recv(1024)
    message_split = re.findall(r"....", message)  # Gather each 4 byte encoded ints in a list.

    ans_int = 0  # The accumulator of all the ints.
    for word in message_split:
        a = struct.unpack("I", word)[0]
        print a
        ans_int += a
    ans_int %= 0xffffffff + 1  # Compensate for integer overflows.

    ans = struct.pack("<I", ans_int)
    connection.send(str(ans))
    print connection.recv(1024)

    connection.close()


if __name__ == "__main__":
    main()

