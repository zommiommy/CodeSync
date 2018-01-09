
import socket

data = "CULOROTTO DIO CARO %d"

i = 0

while True:
	i += 1
	try:
	    host = socket.gethostname()    
	    port = 50420                  
	     # The same port as used by the server
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.connect((host, port))
	    s.sendall((data%i).encode())
	    s.close()
	except:
		print("error")