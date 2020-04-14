import os
import select
import socket
import sys
import time
from termios import tcflush, TCIFLUSH

from questionBank import * #Contains all the questions and options for the quiz
from utilities import * #Contains all the functions which have been called here

os.system('clear')

#Socket programming
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))

#Utility to press buzzer within TIMEOUT limit
def buzzer():
    print(f"\nPress buzzer before everyone else within {TIMEOUT} seconds") 
    pressed = ""

    tcflush(sys.stdin, TCIFLUSH) #Flush any extra input given before the function call

    read , _, _ = select.select([sys.stdin, client_socket],[],[], TIMEOUT) #Checks any responses within the TIMEOUT limit
    #If any response within TIMEOUT seconds
    if read:
        if read[0] == sys.stdin: #If buzzer has been pressed first then read the respomse
            pressed = sys.stdin.readline()
        elif read[0] == client_socket: #Else stop player from pressing buzzer
            message = receiveMsg(client_socket)
            print(message)
            return #Do not remove this!
    #TIMEOUT limit is over
    else:
        print("Time's up!! You can not press buzzer now..\n")

    if pressed == "":
        pressed = "false"
    sendMsg(pressed, client_socket)

#Utility to answer within TIMEOUT limit
def answer():
    print("\nCongratulations!! You pressed the buzzer first..")
    print(f"You have {TIMEOUT} seconds to answer now\n")
    time.sleep(0.5)
    print("Enter option number")
    answer = ""

    tcflush(sys.stdin, TCIFLUSH) #Flush any extra input given before the function call

    read, _, _ = select.select([sys.stdin],[],[], 10) #Checks any responses within the TIMEOUT limit
    #If any response within TIMEOUT seconds
    if read:
        answer = sys.stdin.readline()
    #TIMEOUT limit is over
    else:
        print("Time's up!! You cannot answer now..\n")
    
    if answer == "":
        answer = "false"
    sendMsg(answer, client_socket)   

my_username = input("Enter your usesrname: ") #Player's username
sendMsg(my_username, client_socket)

while True:
    message = receiveMsg(client_socket)
    if message is False:
        continue

    if(message == "Buzzer"):
        buzzer()
    elif(message == "Answer"):
        answer()
    elif(message == "GameOver"):
        break
    else:
        print(message)

#Game is finished
time.sleep(1)
client_socket.close()