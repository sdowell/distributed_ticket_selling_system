import struct

BUY_MESSAGE_CODE = 1

class Message:

	def __init__(self, data):
		self.data_length  = len_data

	def serialize(self):
		pass

	@staticmethod
	def deserialize(self):
		pass


class BuyMessage(Message):

	def serialize(self):
		return struct.pack("!BI", BUY_MESSAGE_CODE, self.num_tickets)

	def __init__(self, num_tickets):
		self.num_tickets = num_tickets
		self.data = self.serialize()
		super(BuyMessage, self).__init__(self.data)

