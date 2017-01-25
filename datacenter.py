import socket
import threading
import socketserver
import sys

import message
import config 

run_server = True

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		data_in = self.request.recv(5)
		cur_thread = threading.current_thread()
		response = 'blah'
		self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	
	def __exit__(self):
		self.shutdown()

def get_kiosk_number():
	if len(sys.argv) < 2:
		print("Not enough args.")
		exit()
	else:
		kiosk_num = int(sys.argv[1])
		return kiosk_num


def handle_message(message):
	message.Message.deserialize(message)


def main():
	print("Start datacenter")
	cfg = config.Config.from_file("config.txt")
	message.TOTAL_KIOSKS = len(cfg.kiosks)
	print(message.TOTAL_KIOSKS)
	kiosk_number = get_kiosk_number()
	server_addr = cfg.kiosks[kiosk_number]
	num_tickets = cfg.num_tickets
	server = ThreadedTCPServer(server_addr, ThreadedTCPRequestHandler)
	server_thread = threading.Thread(target = server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	while run_server:
		pass

if __name__ == "__main__":
	main()
