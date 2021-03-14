# Mustafa Memon
# Alvin Liang
# Maria Leftheriotis
# Ethan Herndon
# CST 311
# Programming Assignment 2 UDP Pinger

from socket import *
import time #Need the time library for time functions

#Declaration of the variables that we will be using
timeOutInt = 0
timeouts = 0
RTT = 0
sumRTT = 0
alpha = 0.125
beta = 0.25
amount = 10
min_rttTime = -1
max_rttTime = -1
estimatedRTT = -1
devRTT = 0
amount_of_pings = 0

serverName = 'localhost' #IP Address
serverPort = 12000 #Port Number
clientSocket = socket(AF_INET, SOCK_DGRAM) #Created socket
clientSocket.settimeout(1) #Packet timer of 1 second if it exceeds the timer then the pings are considered lost

#There are 10 pings that are needed to be sent to the server. We included a loop to iterate the 10 pings to the server.
for x in range(amount): #Loop of sending 10 pings to the server
  index = x + 1 #What number ping is being sent
  message = "Ping" + str(index) #What ping is being sent
  sentTime = time.time() #Time when the packet was sent

  clientSocket.sendto(message.encode(), (serverName, serverPort)) #The server name, port number and message to send into the socket

  #Within our loop we have a try and except if a packet becomes lost we give an alternate way to how it should be approached.
  try: 
    #In the try, this is where our loop will go if packets do not get lost. We also get the time that the packets are recieved where we are able to calculate the round trip time and also able to add up all of round trip times to calculate the total time.
    modifiedMessage, serverAddress = clientSocket.recvfrom(1024) 
    receivedTime = time.time() #Time when packet was received
    RTT = (receivedTime - sentTime) * 1000 #Calculating round trip time in milliseconds

    #In our try we included a if/else statement to calulate our estimatedRTT and devRTT because there are two cases that we have to consider 
    if estimatedRTT == -1: #For first calculation of RTT
      estimatedRTT = RTT #estimatedRTT is set to be equal to the first RTT calculation
      devRTT = RTT/2 #devRTT is set to equal to half of the first RTT calculation 
    else: #Remaining calculations of RTT
      estimatedRTT = (1 - alpha) * estimatedRTT + (alpha * RTT) #Calulation of the estimatedRTT 
      devRTT = (1 - beta) * devRTT + beta * (abs(RTT - estimatedRTT)) #Calculation of the devRTT 
      #devRTT = ((0.75 * devRTT) + (0.25 *abs(RTT - estimatedRTT)))
    
    #Here we have if statements to determine if the previous round trip time is less/greater than the next one if it is less/greater than the previous one that RTT value becomes the new min/max value and if it is not less/greater than the previous value it remains the same.
    if(min_rttTime == -1 or min_rttTime > RTT): #Calculating the minimum Value of RTT
      min_rttTime = RTT
    if(max_rttTime == -1 or max_rttTime < RTT): #Calculating the maximum value of the RTT
      max_rttTime = RTT

    sumRTT += RTT #Adding all of the RTT's together
    amount_of_pings += 1 #Counter for the amount of pings that are received

    #Response of client
    print "Mesg sent: ", message  #If message was sent  
    print "Mesg rcvd: ", modifiedMessage # IF NO TIMEOUT
    print ("PONG %d RTT: %.11f" % (index, RTT)) #ADD RTT TIME for EACH PING  
    print "  "

  #For except this is where the loop will go to if a packet becomes lost. We know if the packet is lost if it exceeds the timer of 1 second. A counter is added to count how many total packets that were lost.
  except timeout: #If packets are lost
    print "Mesg sent: ", message  #If message is sent
    print ("No Mesg rcvd") # IF TIMEOUT HAPPENS 
    print("PONG %d REQUEST TIMED OUT" % index) 
    print "  "
    timeouts += 1 #Counter of how many packets are lost

timeOutInt = estimatedRTT + 4*devRTT #Calculating the timeout interval
timeouts = (timeouts * 100)/amount #Calculating the packet loss

print "Min RTT:             ", min_rttTime,"ms" #The smallest RTT value
print "Max RTT:             ", max_rttTime,"ms" #The largest RTT value
print "Avg RTT:             ", sumRTT / amount_of_pings,"ms" #The average RTT value
print "Packet Loss:          %.1f" %  timeouts #The percentage of packet loss
print "Estimated RTT:       ", estimatedRTT,"ms" #The total value of the estimated RTT
print "Dev RTT:             ", devRTT,"ms" #The total value of the devRTT
print "Timeout Interval:    ", timeOutInt,"ms" #The amount of time the socket waits for data to become available
clientSocket.close()