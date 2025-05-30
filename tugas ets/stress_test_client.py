import socket
import json
import base64
import time
import threading
import concurrent.futures
import os

SERVER_ADDRESS = ('172.16.16.101', 8889)

def send_command(command_str):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVER_ADDRESS)
        sock.sendall(command_str.encode())
        data_received = ''
        while True:
            data = sock.recv(4096)
            if not data:
                break
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                break
        sock.close()
        return json.loads(data_received)
    except Exception as e:
        return {"status":"ERROR", "data": str(e)}

def upload_file(filepath):
    try:
        with open(filepath, "rb") as f:
            filecontent = base64.b64encode(f.read()).decode()
        filename = os.path.basename(filepath)
        command_str = f"UPLOAD {filename} {filecontent}"
        start = time.time()
        hasil = send_command(command_str)
        end = time.time()
        size = os.path.getsize(filepath)
        success = hasil.get('status') == 'OK'
        return success, end-start, size
    except Exception as e:
        return False, 0, 0

def download_file(filename, target_folder="./downloaded"):
    os.makedirs(target_folder, exist_ok=True)
    command_str = f"GET {filename}"
    start = time.time()
    hasil = send_command(command_str)
    end = time.time()
    if hasil.get('status') == 'OK':
        content = hasil.get('data_file')
        data_bytes = base64.b64decode(content)
        with open(os.path.join(target_folder, filename), "wb") as f:
            f.write(data_bytes)
        size = len(data_bytes)
        return True, end-start, size
    else:
        return False, 0, 0

def worker_upload(filepath):
    return upload_file(filepath)

def worker_download(filename):
    return download_file(filename)

def run_stress_test(operation, file_volumes, client_workers, server_workers, concurrency_model):
    """
    operation: 'upload' or 'download'
    file_volumes: list of file paths with different sizes (e.g. ["file_10MB.bin", ...])
    client_workers: number of concurrent client workers (threads or processes)
    server_workers: just metadata here (for documentation; server must be run separately with matching workers)
    concurrency_model: 'thread' or 'process'
    """

    results = []
    import concurrent.futures

    if operation == 'upload':
        work_func = worker_upload
        files = file_volumes
    elif operation == 'download':
        work_func = worker_download
        files = [os.path.basename(f) for f in file_volumes]  # filenames only
    else:
        raise ValueError("Operation must be 'upload' or 'download'")

    # Repeat file list to match client_workers if needed
    total_jobs = client_workers
    jobs = (files * ((total_jobs // len(files)) + 1))[:total_jobs]

    # Select executor
    if concurrency_model == 'thread':
        Executor = concurrent.futures.ThreadPoolExecutor
    else:
        Executor = concurrent.futures.ProcessPoolExecutor

    success_count = 0
    fail_count = 0
    total_bytes = 0
    total_time = 0

    start_test = time.time()
    with Executor(max_workers=client_workers) as executor:
        futures = [executor.submit(work_func, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            try:
                success, duration, size = future.result()
                if success:
                    success_count += 1
                    total_bytes += size
                    total_time += duration
                else:
                    fail_count += 1
            except Exception:
                fail_count += 1

    end_test = time.time()
    elapsed = end_test - start_test
    throughput = total_bytes / total_time if total_time > 0 else 0

    result = {
        'operation': operation,
        'client_workers': client_workers,
        'server_workers': server_workers,
        'concurrency_model': concurrency_model,
        'total_elapsed': elapsed,
        'total_bytes': total_bytes,
        'throughput_bytes_per_sec': throughput,
        'success_clients': success_count,
        'fail_clients': fail_count,
        'file_volume_MB': [os.path.getsize(f)/1024/1024 for f in file_volumes]
    }
    return result

if __name__ == "__main__":
    # Contoh path file 10MB, 50MB, 100MB (harus sudah ada)
    files_10MB = ["file_10MB.bin"]
    files_50MB = ["file_50MB.bin"]
    files_100MB = ["file_100MB.bin"]

    # Buat file dummy (jika belum ada)
    def create_dummy_file(filename, size_mb):
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(os.urandom(size_mb * 1024 * 1024))
    create_dummy_file("file_10MB.bin", 10)
    create_dummy_file("file_50MB.bin", 50)
    create_dummy_file("file_100MB.bin", 100)

    # Contoh run stress test untuk 1 kombinasi
    result = run_stress_test(
        operation='upload',
        file_volumes=files_10MB,
        client_workers=5,
        server_workers=5,
        concurrency_model='thread'
    )
    print(result)
