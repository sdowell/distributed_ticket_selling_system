import socket
import config
import message

def requestTickets(kiosk, tickets):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Attempting to connect to port: " + str(kiosk))
	s.connect((str(kiosk[0]), int(kiosk[1])))
	buy_message = message.BuyMessage(tickets)
	s.send(buy_message.data)
	response = s.recv(16)
	success = message.Message.deserialize(response)
	s.close()
	return success

def cmdUI(cfg):
	done = False
	while not done:
		#print information
		i = 0
		for k in cfg.kiosks:
			print(str(i) + ". " + str(k))
			i = i + 1
		print(str(i) + ". exit")
		#ask user for kiosk to connect to
		try:
			a_input = input("Please choose a kiosk or exit: ")
		except NameError:
			print("Invalid input: expected int")
			continue
		try:
			a_input = int(a_input)
		except ValueError:
			print("Invalid input")
			continue
		if a_input < 0 or a_input > i:
			print("Input out of range")
			continue
		if a_input == i:
			done = True
			break
		myKiosk = a_input
		#ask user for number of tickets
		buytickets = input("How many tickets would you like to purchase? ")
		try:
			buytickets = int(buytickets)
		except ValueError:
			print("Invalid input")
			continue
		#request to purchase tickets from selected kiosk
		success = requestTickets(cfg.kiosks[myKiosk], buytickets)
		if success == message.BUY_SUCCESS:
			print("Tickets purchased successfully")
		elif success == message.BUY_FAIL:
			print("Tickets not purchased")
		else:
			print("Error: unrecognized response")
		

def main():
	print("Starting client...")
	cfg = config.Config.from_file("config.txt")
	cmdUI(cfg)
	exit()


if __name__ == "__main__":
	main()

