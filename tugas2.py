from socket import 
import socket
import threading
import logging
from datetime import datetime

# Thread untuk memproses setiap klien
class ProcessTheClient(threading.Thread)
    def __init__(self, connection, address)
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self)
        try
            while True
                data = self.connection.recv(1024)
                if not data
                    break

                # Decode data dan strip karakter rn
                message = data.decode('utf-8').strip('rn')
                logging.warning(fReceived from {self.address} {message})

                if message.startswith(TIME)
                    now = datetime.now()
                    current_time = now.strftime(%H%M%S)
                    response = fJAM {current_time}rn
                    self.connection.sendall(response.encode('utf-8'))

                elif message == QUIT
                    logging.warning(fClient {self.address} requested to quit.)
                    break

                else
                    logging.warning(fInvalid request from {self.address} {message})
        except Exception as e
            logging.error(fError handling client {self.address} {e})
        finally
            self.connection.close()
            logging.warning(fConnection closed {self.address})

# Server class
class Server(threading.Thread)
    def __init__(self)
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self)
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning(Server is listening on port 45000...)

        while True
            connection, client_address = self.my_socket.accept()
            logging.warning(fConnection from {client_address})

            client_thread = ProcessTheClient(connection, client_address)
            client_thread.start()
            self.the_clients.append(client_thread)

def main()
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    server = Server()
    server.start()

if __name__ == __main__
    main()
