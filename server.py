import socket, sys, select
from threading import Thread
from Queue import Queue

# define broadcastMsg
def broadcastMsg(sock, message):
	for socket in CONNECT_LIST:
		if socket != server_socket and socket != sock:
			try:
				socket.send(message)
			except:
				socket.close()
				CONNECT_LIST.remove(socket)

def worker():
	pass

if __name__ == "__main__":

	host = socket.gethostname()
	port = 9999
	CONNECT_LIST = []
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# bind socket and listen
	try:
		server_socket.bind((host, port))
	except socket.error, msg:
		print "Can't bind. Error code: " + str(msg[0]) + ", Message " + msg[1]
		sys.exit()	
	print 'Socket bind success, ' + str(host)
	server_socket.listen(5)
	CONNECT_LIST.append(server_socket)
	print 'Listening to connection requests...'

	# connect to clients
	while True:
		socket_list = [sys.stdin, server_socket]
		read_sockets, write_sockets, error_sockets = select.select(CONNECT_LIST, [], [])
		for sock in read_sockets:
			if sock == server_socket:
				conn, addr = server_socket.accept()		
				CONNECT_LIST.append(conn)
				print "Connected with <" + addr[0] + ", " + str(addr[1]) + ">"
				broadcastMsg(conn, "[%s, %s] entered the chat\n" % addr)
			else:
				try:
					data = sock.recv(1024)
					if data:
						broadcastMsg(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
				except:
						broadcastMsg(sock, "Client (%s, %s) is offline" % addr)
						print "DCed with <%s, %s>" % addr
						sock.close()
						CONNECT_LIST.remove(sock)
						continue
	server_socket.close()