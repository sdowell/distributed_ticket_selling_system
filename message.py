import struct
from math import floor, ceil
BUY_MESSAGE_CODE = 1
BUY_MESSAGE_RESPONSE_CODE = 2
BUY_SUCCESS = 1
BUY_FAIL = 0
REQUEST_MESSAGE_CODE = 3
TOTAL_KIOSKS = None 

class Message:

	def __init__(self, data):
		self.data = data
		self.data_length  = len(data)

	def serialize(self):
		pass

	@staticmethod
	def deserialize(data):
		#print(str(type(data)))
		#print(str(len(data)))
		message_type = struct.unpack("!B",data[0:1])
		if message_type == BUY_MESSAGE_CODE:
			return BuyMessage.deserialize(data)
		elif message_type == BUY_MESSAGE_RESPONSE_CODE:
			return BuyMessageResponse.deserialize(data)
		elif message_type == REQUEST_MESSAGE_CODE:
			return RequestMessage.deserialize(data)
		else: #other message types
			pass

class RequestMessage(Message):
	
	def serialize(self):
		return struct.pack("!Bf", REQUEST_MESSAGE_CODE, (float(self.lamport_clock) + float(self.pid)/self.total_kiosks))

	def __init__(self, lamport_clock, process_id):
		self.lamport_clock = lamport_clock
		self.pid = process_id
		self.rank = (float(self.lamport_clock) + float(self.pid)/TOTAL_KIOSKS)
		super(RequestMessage, self).__init__(self.serialize())
	
	@staticmethod
	def deserialize(data):
		msg_code, fpoint = struct.unpack("!Bf", data)
		assert msg_code == REQUEST_MESSAGE_CODE
		lamport_clock = floor(fpoint)
		process_id = (float(fpoint)-float(lamport_clock))*float(TOTAL_KIOSKS)
		process_id = int(round(process_id))
		return RequestMessage(lamport_clock, process_id)
		
	

class BuyMessage(Message):

	def serialize(self):
		return struct.pack("!BI", BUY_MESSAGE_CODE, self.num_tickets)

	def __init__(self, num_tickets):
		self.num_tickets = num_tickets
		super(BuyMessage, self).__init__(self.serialize())

	@staticmethod
	def deserialize(data):
		num_tickets = struct.unpack("!I",data[1:5])
		return BuyMessage(num_tickets)

class BuyMessageResponse(Message):

	def serialize(self):
		return struct.pack("!BI", BUY_MESSAGE_RESPONSE_CODE, self.success)

	def __init__(self, successful):
		if successful is True:
			self.success = BUY_SUCCESS
		else:
			self.success = BUY_FAIL
		super(BuyMessageResponse, self).__init__(self.serialize())
	
	@staticmethod
	def deserialize(data):
		success = struct.unpack("!I", data[1:5])
		return BuyMessageResponse(success == BUY_SUCCESS)
	


