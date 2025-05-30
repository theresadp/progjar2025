import socket

def main():
    server_address = ('172.16.16.101', 45000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(server_address)
        print("Terhubung ke server time.")

        while True:
            print("\nKetik 'TIME' untuk meminta jam, 'QUIT' untuk keluar.")
            user_input = input("Masukkan perintah: ").strip().upper()

            if user_input in ["TIME", "QUIT"]:
                message = f"{user_input}\r\n"
                client_socket.sendall(message.encode('utf-8'))

                if user_input == "TIME":
                    response = client_socket.recv(1024).decode('utf-8').strip()
                    print(f"Respons dari server: {response}")
                elif user_input == "QUIT":
                    print("Keluar dari server.")
                    break
            else:
                print("Perintah tidak dikenal. Gunakan 'TIME' atau 'QUIT'.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
