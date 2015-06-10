import socket, sys, wx, select

host  = socket.gethostname()
port = 9999

def sendPicture():
	pass

def prompt():
	sys.stdout.write("<ME> ")
	sys.stdout.flush()

if __name__ == "__main__":
	#create socket
	try:
		clinet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clinet_socket.settimeout(5)
	except socket.error, msg:
		print 'Cannot create socket, error code ' + str(msg[0]) + ': ' + msg[1]
		sys.exit()

	#connect to server
	try:
		clinet_socket.connect((host, port))
	except socket.error:
		print "Can't reach the server, closing program..."
		sys.exit()
	prompt()
	
	#Message loop
	while True:
		socket_list = [sys.stdin, clinet_socket]
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
		for sock in read_sockets:
			if sock == clinet_socket:
				data = sock.recv(1024)
				if not data:
					print "\nServer is down"
					sys.exit()
				else:
					sys.stdout.write(data)
					prompt()
			else:
				message = sys.stdin.readline()
				if message == '':
					continue					
				clinet_socket.send(message)
				prompt()