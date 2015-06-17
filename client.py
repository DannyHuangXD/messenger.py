import socket, sys, wx, select

host = socket.gethostname()
port = 9999

def sendPicture():
	address = (host, 9998)
	udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	fileDir = raw_input("FileRoute: ")
	fileContent = open(fileDir, 'rb')
	file_data = fileContent.read()
	file_frags = [file_data[i: i + 1024] for i in range(0, len(file_data), 1024)]
	for x in file_frags:
		udp_s.sendto(x, address)
	udp_s.sendto("end", address)
	print "Picture sent."
	prompt()

def receivePicture(sock):
	pic_data = sock.recv()
	print "!" + pic_data
	fp = open("imager.jpg", ab)
	fp.write(pic_data)
	fp.close()


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
				if data == "i.ppic":
					receivePicture(sock)
				elif not data:
					print "\nLost connection to the server"
					print data
					sys.exit()
				else:
					sys.stdout.write(data)
					prompt()
			else:
				message = sys.stdin.readline()
				if message == '':
					continue
				clinet_socket.send(message)
				if message == 'i.pic\n':
					sendPicture()
					continue
				prompt()