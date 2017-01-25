import socket
import config

def requestTickets(kiosk, tickets):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', int(kiosk)))
	s.send('buy ' + str(tickets))
	response = s.recv(1024)
	s.close()
	return response

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
		a_input = input("Please choose a kiosk or exit: ")
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
		response = requestTickets(myKiosk, buytickets)

def main():
	print("Starting client...")
	cfg = config.Config.from_file("config.txt")
	cmdUI(cfg)
	exit()


if __name__ == "__main__":
	main()

