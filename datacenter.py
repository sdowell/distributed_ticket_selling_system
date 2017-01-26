import socket
import threading
import socketserver
import sys
import queue
import select

import message
import config 

run_server = True
#server priority queue
pq = queue.PriorityQueue()
pq_lock = threading.RLock()
lclock = 0
lclock_lock = threading.RLock()
cfg = None
tickets = None
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		data_in = self.request.recv(5)
		cur_thread = threading.current_thread()
		response_message = handle_message(data_in)
		if response_message is not None:
			self.request.sendall(response_message.serialize())

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


def sync_lclock(clock_val = None):
	global lclock
	with lclock_lock:
		if clock_val is not None and clock_val >= lclock:
			lclock = clock_val + 1
		else:
			lclock = lclock + 1

def handle_message(recv_message):
	global tickets
	our_message = message.Message.deserialize(recv_message)
	print(str(our_message))
	if type(our_message) is message.RequestMessage:
		our_request_message = our_message
		sync_lclock(our_message.lamport_clock)
		pq.put((our_request_message.rank, our_request_message))
		return message.ReplyMessage()
	elif type(our_message) is message.BuyMessage:
		print("GOT BUY MESSAGE")
		our_buy_message = our_message
		our_sockets = [None]*message.TOTAL_KIOSKS
		readers, writers, errors = [],[],[]
		release_writers = []
		with lclock_lock:
			sync_lclock()
			pq.put((message.get_rank( lclock, get_kiosk_number()),our_buy_message))
			for x in range(0, message.TOTAL_KIOSKS):
				if x is not get_kiosk_number():
					our_sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					our_sockets[x].connect(cfg.kiosks[x])
					our_sockets[x].setblocking(0)
					writers.append(our_sockets[x])
					readers.append(our_sockets[x])
					release_writers.append(our_sockets[x])
			while len(writers) != 0:
				_ , pwriters , _ = select.select(readers, writers, errors)
				for writer in pwriters:
					writer.send(message.RequestMessage(lclock, get_kiosk_number()).data)
					writers.remove(writer)
			while len(readers) != 0:
				preaders, _ , _ = select.select(readers, writers, errors)
				for reader in preaders:
					data_in = reader.recv(5)
					message_in = message.Message.deserialize(data_in)
					assert type(message_in) is message.ReplyMessage
					readers.remove(reader)
		recvd = False
		while recvd == False:
			with pq_lock:
				our_tuple = pq.get()
				if our_tuple[1] == our_buy_message:
					recvd = True
					success = None
					if our_buy_message.num_tickets <= tickets:
						success = True
						tickets -= our_buy_message.num_tickets
					else:
						success = False
					while len(release_writers) != 0:
						_, pwriters, _ = select.select([],release_writers, [])
						for writer in pwriters:
							writer.send(message.ReleaseMessage(tickets).data)
							release_writers.remove(writer)
					return message.BuyMessageResponse(success)
				else:
					pq.put(our_tuple)
					sleep(1)
	elif type(our_message) is message.ReleaseMessage:
		tickets = our_message.num_tickets
		pq.get() #scary
		return None


def main():
	print("Start datacenter")
	global cfg
	cfg  = config.Config.from_file("config.txt")
	global tickets
	tickets = cfg.tickets
	message.TOTAL_KIOSKS = len(cfg.kiosks)
	print(message.TOTAL_KIOSKS)
	kiosk_number = get_kiosk_number()
	server_addr = cfg.kiosks[kiosk_number]
	num_tickets = cfg.tickets
	server = ThreadedTCPServer(server_addr, ThreadedTCPRequestHandler)
	server_thread = threading.Thread(target = server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	while run_server:
		pass

if __name__ == "__main__":
	main()
