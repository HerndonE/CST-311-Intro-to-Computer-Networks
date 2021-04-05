# Ethan Herndon
# Mustafa Memon
# Maria Leftheriotis
# Alvin Liang
# Programming Assignment 3: TCP Client Server

'''
-Explain why you need multithreading to solve this problem. Put this in a comment at the top of your server code-

For this code you need to have a multithreaded server so you are be able to have two connections that are able to send data to the one server. The two parts are running simultaneously for data to be sent between the connections. The multithreaded server allows for the two connections to communicate with the one server. Each connection has its own thread and one connection does not need to wait for the other connection to end.
'''

#TCPCapitalizationServer.py
from socket import *
import threading #Needed to initiate a multithreaded server
import time #For time functions

serverName = gethostname() #Computer's hostname, IP address
serverPort = 12000 #Port number

#Declarations of variables
socket_X = -1
socket_Y = -1
message_X = -1
message_Y = -1
message_number = 1
clientFirst = [] # stores the clients in order of when they send a message
messageFirst = [] # stores the messages in order of when sent
connected_X = 'Client X connected'
connected_Y = 'Client Y connected'

#We have defined the function get_message to help with the multithreaded server
def get_message(clientFrom, clientTo, socketFrom, socketTo):
  #Able to reach the below variables outside the function
  global message_number 
  global clientFirst  
  global messageFirst

  message = socketFrom.recv(1024).decode() 

  clientFirst.append(clientFrom) #Counts up the clients of when they send the message
  messageFirst.append(message) #Counts up the messages of the order

  print("Client %s sent message %d: %s" % (clientFrom, message_number, message)) #Tells the order of which client sent what message first and second
  message_number = message_number + 1 #Counts the number of messages

#Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM) #Notice the use of SOCK_STREAM for TCP packets
serverSocket.bind((serverName, serverPort)) #Assign IP address and port number to socket

print ('The server is ready to receive 2 connections....\n')
serverSocket.listen(2) #Listens for two connections

while (socket_X == -1): #For First Connection
  socket_X, addr = serverSocket.accept() #Creating First Connection socket for server to accept
  print ('Accepted first connection, calling it client X')
 
while (socket_Y == -1): #For Second Connection
  socket_Y, addr = serverSocket.accept() #Creating Second Connection socket for server to accept
  print ('Accepted second connection, calling it client Y')

print ('\nWaiting to receive messages from client X and client Y....\n') #Lets the client know that the server is waiting for messages

#Tells the client the connection is connected and lets the client know which connection is which
socket_X.send(connected_X.encode())
socket_Y.send(connected_Y.encode())

#Here we create two threads for the connections to be able to run simultaneously
thread_1 = threading.Thread(target=get_message,args=('X','Y',socket_X,socket_Y))
thread_2 = threading.Thread(target=get_message,args=('Y','X',socket_Y,socket_X))

#Starting the two threads
thread_1.start()
thread_2.start()

#Let the threads be able to communicate to the server while running simultaneously and then lets the threads close
thread_1.join()
thread_2.join()

#Here we have a format to tell us what client sent the first message
#0 is the first connection that sent a message 
#1 is the second connection that sent a message
sentence = "From Server: "
sentence = sentence + clientFirst[0] + ": "
sentence = sentence + messageFirst[0] + " received before "
sentence = sentence + clientFirst[1] + ": "
sentence = sentence + messageFirst[1]

#Sends the message to the client to show the order of which the server recieved the messages
socket_Y.send(sentence.encode()) 
socket_X.send(sentence.encode())

#Closing both sockets
print ('\nWaiting a bit for clients to close their connections')
time.sleep(1) #Timer
socket_X.close(); #Closing socket_X
socket_Y.close(); #Closing socket_Y

print('Done.') #Acknowledegment that the sockets closed