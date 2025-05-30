import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from file_protocol import FileProtocol

fp = FileProtocol()

def handle_client(connection, address):
    logging.warning(f"connected from {address}")
    try:
        data_received = ''
        while True:
            data = connection.recv(1024)
            if not data:
                break
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                break

        if data_received:
            response = fp.proses_string(data_received.strip())
            connection.sendall((response + "\r\n\r\n").encode())
    finally:
        connection.close()

def main():
    logging.basicConfig(level=logging.WARNING)
    server_address = ('0.0.0.0', 8889)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(5)
    logging.warning(f"Server thread pool listening on {server_address}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            conn, addr = sock.accept()
            executor.submit(handle_client, conn, addr)

if __name__ == "__main__":
    main()
