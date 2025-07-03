import socket
import logging

# Ganti IP sesuai dengan IP server kamu
server_address = ('192.168.1.100', 8889)

def make_socket(destination_address='localhost', port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((destination_address, port))
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def send_command(command_str):
    alamat_server = server_address[0]
    port_server = server_address[1]
    sock = make_socket(alamat_server, port_server)

    try:
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(2048)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        return data_received
    except Exception as ee:
        logging.warning(f"error during receiving: {str(ee)}")
        return False
    finally:
        sock.close()

if __name__ == '__main__':
    # Tes salah satu command
    # 1. List file
    # cmd = "GET /list HTTP/1.0\r\n\r\n"

    # 2. Upload file
    # cmd = "POST /upload HTTP/1.0\r\nFilename: coba.txt\r\nContent: ini isi file\r\n\r\n"

    # 3. Delete file
    # cmd = "POST /delete HTTP/1.0\r\nFilename: coba.txt\r\n\r\n"

    cmd = "GET /list HTTP/1.0\r\n\r\n"  # contoh aktif
    hasil = send_command(cmd)
    print(hasil)
