import socket

def requestTickets(kiosk, tickets):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', str(kiosk)))
	s.send('buy ' + str(tickets))
	
	response = s.recv(1024)
	return response

def cmdUI(kiosks, delay, numtickets):
	done = false
	while not done:
		#print information
		i = 0
		for k in kiosks:
			print str(i) + ". " + str(k)
			i = i + 1
		print str(i) + ". exit"
		#ask user for kiosk to connect to
		input = raw_input("Please choose a kiosk or exit: ")
		try:
			input = int(input)
		except ValueError:
			print "Invalid input"
			continue
		if input < 0 or input > i:
			print "Input out of range"
			continue
		if input == i:
			done = true
			break
		myKiosk = input
		#ask user for number of tickets
		buytickets = raw_input("How many tickets would you like to purchase? ")
		try:
			buytickets = int(buytickets)
		except ValueError:
			print "Invalid input"
			continue
		#request to purchase tickets from selected kiosk
		response = requestTickets(myKiosk, buytickets)
		print response
def main:
	print "Start client"
	with open("config.txt") as f:
		lines = f.readlines()
	kiosks = []
	delay = None
	numtickets = None
	for line in lines:
		spl = line.split()
		if spl[0] == "kiosk":
			kiosks.append(int(spl[1]))
		elif spl[0] == "tickets":
			numtickets = int(spl[1])
		elif spl[0] == "delay":
			delay = int(spl[1])
	if len(kiosks) == 0:
		print "Error: no kiosks found in config file"
		exit()
	if delay == None:
		print "Error: no delay found in config file"
		exit()
	if numtickets == None:
		print "Error: tickets not found in config file"
		exit()
	cmdUI(kiosks, delay, numtickets)
	exit()

if __name__ == "__main__":
	main()
