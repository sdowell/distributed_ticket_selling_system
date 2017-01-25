import struct

BUY_MESSAGE_CODE = 1
BUY_MESSAGE_RESPONSE_CODE = 2
BUY_SUCCESS = 1
BUY_FAIL = 0

class Message:

	def __init__(self, data):
		self.data = data
		self.data_length  = len(data)

	def serialize(self):
		pass

	@staticmethod
	def deserialize(self, data):
		message_type = struct.unpack("!B",data[0:1])
		if message_type == BUY_MESSAGE_CODE:
			return BuyMessage.deserialize(data)
		elif message_type == BUY_MESSAGE_RESPONSE_CODE:
			return BuyMessageResponse.deserialize(data)
		else: #other message types
			pass


class BuyMessage(Message):

	def serialize(self):
		return struct.pack("!BI", BUY_MESSAGE_CODE, self.num_tickets)

	def __init__(self, num_tickets):
		self.num_tickets = num_tickets
		super(BuyMessage, self).__init__(self.serialize())

	@staticmethod
	def deserialize(self, data):
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
	def deserialize(self, data):
		success = struct.unpack("!I", data[1:5])
		return BuyMessageResponse(success == BUY_SUCCESS)
	


