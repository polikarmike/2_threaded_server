import socket

def start_client(host='127.0.0.1', port=9090):
    """Простой клиент для тестирования эхо-сервера."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("[INFO] Connected to the server. Type messages to send. Type 'exit' to close.")
    try:
        while True:
            message = input("> ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"[SERVER]: {response}")
    except KeyboardInterrupt:
        print("\n[INFO] Disconnected.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
