# Mustafa Memon
# Alvin Liang
# Maria Leftheriotis
# Ethan Herndon
# CST 311
# Programming Assignment 2 UDP Pinger

# Server.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
 
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('localhost', 12000))
print("Waiting for Client....\n")
 
while True:
    # Generate random number5 in the range of 0 to 10
    rand = random.randint(0, 10)   

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
          continue

    # Otherwise, the server responds 
    modifiedMessage = message.upper()
    print modifiedMessage, " Received"
    print "Mesg rcvd: ", message
    print "Mesg sent: ", modifiedMessage, "\n" 
    serverSocket.sendto(modifiedMessage, address)