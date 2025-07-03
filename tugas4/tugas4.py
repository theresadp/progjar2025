import os
from glob import glob
from datetime import datetime

class HttpServer:
    def __init__(self):
        self.types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.txt': 'text/plain',
            '.html': 'text/html'
        }

    def response(self, kode=404, message='Not Found', messagebody=bytes(), headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = []
        resp.append(f"HTTP/1.0 {kode} {message}\r\n")
        resp.append(f"Date: {tanggal}\r\n")
        resp.append("Connection: close\r\n")
        resp.append("Server: myserver/1.0\r\n")
        resp.append(f"Content-Length: {len(messagebody)}\r\n")
        for kk in headers:
            resp.append(f"{kk}: {headers[kk]}\r\n")
        resp.append("\r\n")

        response_headers = ''.join(resp)
        if not isinstance(messagebody, bytes):
            messagebody = messagebody.encode()
        return response_headers.encode() + messagebody

    def proses(self, data):
        requests = data.split("\r\n")
        if not requests:
            return self.response(400, 'Bad Request', '', {})

        baris = requests[0]
        all_headers = [h for h in requests[1:] if h.strip()]
        try:
            method, address, _ = baris.strip().split()
            method = method.upper()
            if method == 'GET':
                return self.http_get(address, all_headers)
            elif method == 'POST':
                return self.http_post(address, all_headers)
            else:
                return self.response(400, 'Bad Request', '', {})
        except Exception:
            return self.response(400, 'Bad Request', '', {})

    def http_get(self, object_address, headers):
        if object_address == '/':
            return self.response(200, 'OK', 'Selamat datang di server', {})

        if object_address == '/list':
            files = os.listdir('./')
            body = '\n'.join(files)
            return self.response(200, 'OK', body, {'Content-type': 'text/plain'})

        path = '.' + object_address
        if not os.path.exists(path):
            return self.response(404, 'Not Found', '', {})

        with open(path, 'rb') as fp:
            isi = fp.read()

        fext = os.path.splitext(path)[1]
        content_type = self.types.get(fext, 'application/octet-stream')
        headers = {'Content-type': content_type}
        return self.response(200, 'OK', isi, headers)

    def http_post(self, object_address, headers):
        if object_address == '/upload':
            filename, content = '', ''
            for h in headers:
                if h.lower().startswith('filename:'):
                    filename = h.split(':', 1)[1].strip()
                elif h.lower().startswith('content:'):
                    content = h.split(':', 1)[1].strip()

            if not filename or not content:
                return self.response(400, 'Bad Request', 'Missing filename or content', {})
            with open(filename, 'w') as f:
                f.write(content)
            return self.response(200, 'OK', f'File {filename} uploaded successfully', {})

        elif object_address == '/delete':
            filename = ''
            for h in headers:
                if h.lower().startswith('filename:'):
                    filename = h.split(':', 1)[1].strip()
            if not filename:
                return self.response(400, 'Bad Request', 'Missing filename', {})
            if not os.path.exists(filename):
                return self.response(404, 'Not Found', 'File not found', {})
            os.remove(filename)
            return self.response(200, 'OK', f'File {filename} deleted successfully', {})

        return self.response(404, 'Not Found', 'Unknown POST target', {})
