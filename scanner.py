import socket
from threading import Thread, Lock
from queue import Queue
from tqdm import tqdm  # Для progress bar

# Глобальные переменные
lock = Lock()
open_ports = []
progress = None


def scan_port(host, port):
    """Попытка подключиться к указанному порту."""
    global progress
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)  # Таймаут на подключение
            sock.connect((host, port))
            with lock:
                open_ports.append(port)
    except:
        pass
    finally:
        if progress:
            progress.update(1)


def worker(host, queue):
    """Потоковый обработчик для сканирования портов."""
    while not queue.empty():
        port = queue.get()
        scan_port(host, port)
        queue.task_done()


def port_scanner(host, start_port, end_port, num_threads=100):
    """Запуск сканера портов с многопоточностью."""
    global progress

    # Создание очереди задач
    port_queue = Queue()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Настройка progress bar
    progress = tqdm(total=end_port - start_port + 1, desc="Scanning ports", unit="port")

    # Запуск потоков
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=worker, args=(host, port_queue))
        thread.start()
        threads.append(thread)

    # Ожидание завершения всех задач
    port_queue.join()

    # Закрытие progress bar
    progress.close()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    # Возвращение списка открытых портов
    return sorted(open_ports)


if __name__ == "__main__":
    target_host = input("Enter the host/IP to scan: ").strip()
    start = int(input("Enter the starting port: "))
    end = int(input("Enter the ending port: "))

    print("[INFO] Scanning ports...")
    open_ports = port_scanner(target_host, start, end)
    print(f"[INFO] Open ports on {target_host}: {open_ports}")
