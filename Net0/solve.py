import socket  # Makes connection to the server.
import struct  # Packs integers into a byte string.
import re      # Responsible for filtering the string for the number.


def print_info(message):
    print "[i] " + message


def print_err(message):
    print "[X] " + message


def print_warn(message):
    print "[!] " + message


def main():
    print_info("Attempting to connect...")
    connection = socket.socket()  # Create a socket object to interract with the server.
    connection.connect(("192.168.206.132", 2999))  # Connecting.
    print_info("Connected successfully!")

    pattern = r"'\d*'"  # Searches for numbers of any length within single quotes.
    message = connection.recv(1024)  # Recieves at most 1024B.

    filtered_str = re.findall(pattern, message)[0]  # Filter the string for the number.
    decimal = int(filtered_str[1:len(filtered_str)-1])  # Convert the string to the actual number.

    payload = struct.pack("<L", decimal)  # Get the byte string in little-endian format.

    print_info("Sending payload...")
    connection.send(payload)  # Send the payload to the server.
    print_info("Server accepted payload!")

    print connection.recv(1024)  # Recieve the success message.

    connection.close()  # Free system resources.


if __name__ == "__main__":
    main()

