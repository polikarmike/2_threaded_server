import socket
import threading


def handle_client(conn, addr):
    """Обработка соединения с клиентом."""
    print(f"[INFO] New connection from {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{addr}] {data.decode()}")
            conn.send(data)  # Эхо-ответ
        except Exception as e:
            print(f"[ERROR] Error with client {addr}: {e}")
            break
    conn.close()
    print(f"[INFO] Connection with {addr} closed.")


def start_server(host='0.0.0.0', port=9090):
    """Запуск многопоточного эхо-сервера."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[INFO] Server is listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
