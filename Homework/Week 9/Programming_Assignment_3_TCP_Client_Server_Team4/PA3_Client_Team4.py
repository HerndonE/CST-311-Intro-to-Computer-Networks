# Ethan Herndon
# Mustafa Memon
# Maria Leftheriotis
# Alvin Liang
# Programming Assignment 3: TCP Client Server

from socket import *

serverName = gethostname() #Computer's hostname
serverPort = 12000 #Port number

clientSocket = socket(AF_INET, SOCK_STREAM) #Created Socket 
clientSocket.connect((serverName,serverPort)) #Socket connects to the host and the port number

#Tells that each client is connected
connected = clientSocket.recv(1024)
print "From Server: " + connected.decode()

#Tells the connections that they can enter messages and allows for messages to be entered
sentence = raw_input('Enter message to send to server: ')
clientSocket.send(sentence.encode())

#Tells the order of which connection sent a message first
acknowledgementMessage = clientSocket.recv(1024)
print(acknowledgementMessage.decode())

clientSocket.close() #Closes the client sockets