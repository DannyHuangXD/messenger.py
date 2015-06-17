import socket, sys, select
from threading import Thread
from Queue import Queue
from PIL import Image


# define broadcastMsg
def broadcastMsg(sock, message):
	for socket in CONNECT_LIST:
		if socket != server_socket and socket != sock:
			try:
				socket.send(message)
			except:
				socket.close()
				CONNECT_LIST.remove(socket)

def broadcastPic(sock, message, pic_bin):
	print "Broadcasting picture\n"
	for socket in CONNECT_LIST:
		if socket != server_socket and socket != sock:
				socket.send("i.ppic")
				print "send"
				file_frags = [file_data[i: i + 1024] for i in range(0, len(file_data), 1024)]
				for x in file_frags:
					socket.send(x)


def createChatRoom(sock):
	pass

def getPic():
	address = (socket.gethostname(), 9998)
	udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_s.bind(address)
	while True:
		pic_frag, addr = udp_s.recvfrom(1024)
		if pic_frag == 'end':
			break
		fp = open("image.png", "ab")
		fp.write(pic_frag)
		fp.close()
	udp_s.close()

if __name__ == "__main__":
	host = socket.gethostname()
	port = 9999
	msgLength = 2048
	CONNECT_LIST = []
	CHATROOM_LIST = []
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# bind socket and listen
	try:
		server_socket.bind((host, port))
	except socket.error, msg:
		print "Can't bind. Error code: " + str(msg[0]) + ", Message " + msg[1]
		sys.exit()	
	print 'Socket bind success, ' + str(host) + ", " + str(port)
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
					data = sock.recv(msgLength)
					if data:
						broadcastMsg(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
					if data == 'i.cc\n':
						createChatRoom(sock)
					if data == 'i.pic\n':
						getPic()
						#pic_data = open("/Users/dhxd/Desktop/messenger.py/image.jpg", rb)
						#pic_bin = pic_data.read()
						#broadcastPic(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + "Picture sent", pic_bin)
				except:
						broadcastMsg(sock, "Client (%s, %s) is offline" % addr)
						print "Disconnected with <%s, %s>" % addr
						sock.close()
						CONNECT_LIST.remove(sock)
						continue
	server_socket.close()