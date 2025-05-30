import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""



class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
    def proses_string(self, string_datamasuk=''):
    	logging.warning(f"string diproses: {string_datamasuk[:50]}...")  # log potongan saja
    	try:
        	# manual split karena shlex gagal untuk base64 panjang
        	tokens = string_datamasuk.split(' ', 2)
        	c_request = tokens[0].strip().lower()
        	logging.warning(f"memproses request: {c_request}")

        	if c_request == "upload":
            		filename = tokens[1]
            		filedata_base64 = tokens[2]
            		params = [filename, filedata_base64]
        	elif c_request == "delete":
            		params = [tokens[1]]
        	elif c_request == "get":
            		params = [tokens[1]]
        	else:
            		params = []

        	cl = getattr(self.file, c_request)(params)
        	return json.dumps(cl)
    	except Exception as e:
        	logging.error(f"Error in proses_string: {str(e)}")
        	return json.dumps(dict(status='ERROR', data='request tidak dikenali'))


if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))