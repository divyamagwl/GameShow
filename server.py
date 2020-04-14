import os
import select
import socket
import time

from questionBank import * #Contains all the questions and options for the quiz
from utilities import * #Contains all the functions which have been called here

os.system('clear')

#Socket programming
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(3)

print("Server started ...")

max_players = 3 #Maximum number of players (Flexible.. Change it according to your wish)
max_score = 5 #Maximum score to win the game (Flexible.. Change it according to your wish)

sockets_list = [s] 
players = {}
scores_list = {}

asked_que = [False]*len(questions_list) #List of questions which have already been asked 
index = -1 #index of the question in questionBank
display_options = [] #order of the current options being displayed (Option numbers are shuffled everytime)
questions = 0 #Total number of questions asked

#Utility to accept connections to the server
def accept_connections():
    while len(players) < max_players: #Connections need to be equal to max_players
        conn, addr = s.accept() #Accepting new connections
        username = receiveMsg(conn) #Receiving username of the new client
        if username is False:
            continue

        sockets_list.append(conn) #List of all sockets connected
        players[conn] = username #List of all players
        scores_list[username] = 0 #Scores of all players

        print(f"Accepted new connection {addr}")
        print(f"Player username is {username}")
        sendMsg("\nWaiting for other players to connect...\n", conn)

#Utility to send message to all the clients at once
def broadcast(message):
    for connection in sockets_list:
        try:
            sendMsg(message, connection)
        except:
            pass

#Utility to send question and options of the quiz to all players
def quiz():
    global index, display_options 
    index = selectQuestion(asked_que) #Selecting a random question which has not been asked earlier
    display_options = displayOptions(index) #Shuffled options
    broadcast(f"\nQ. {questions_list[index]}\n") 
    #time.sleep(0.5)

    option_num = 1
    for option in display_options:
        broadcast(f"{option_num}. {option}")
        option_num += 1

    broadcast("Buzzer") #Indicates the client to press buzzer

#Utility to display scores of all the players
def scoreTable():
    time.sleep(1)
    broadcast("\nCurrent Scores")
    for player in scores_list:
        broadcast(f"{player} : {scores_list[player]}")

#Utility to check if the answer is correct or not
def checkAnswer(option, buzzer_player):
    global display_options, index
    correct = False 
    time.sleep(0.5)

    if option == "false": #Indication from the client that no response was given within 10 seconds
        sendMsg("You get -0.5 score", buzzer_player)
    elif (49 <= ord(option[0]) <= 52): #ASCII value from 1 to 4
        option = int(option)
        correct = checkOption(display_options, option, index)
    else: #If something else is input then the answer is considered to be wrong
        pass

    if correct:
        sendMsg("\nYour answer is correct", buzzer_player)
        sendMsg("You get +1 score", buzzer_player)
        scores_list[players[buzzer_player]] += 1
    else:
        sendMsg("\nYour answer is wrong", buzzer_player)
        sendMsg("You get -0.5 score", buzzer_player)
        scores_list[players[buzzer_player]] -= 0.5

    if scores_list[players[buzzer_player]] >= max_score:
        return True
    return False


accept_connections()
time.sleep(0.5)
broadcast(f"All players have joined the game..")
time.sleep(1)

#Game Rules
broadcast(f"\nRules of the quiz are simple -") 
broadcast(f"You have 10 seconds to press buzzer(enter any letter or number on the keyboard).")
broadcast(f"The first one to press buzzer will be given the opportunity to answer")
broadcast(f"You have 10 seconds to answer if your answer is correct you get +1 , in all other cases -0.5")
broadcast(f"First one to reach 5 points will be declared as the winner")
time.sleep(5)
broadcast(f"\nGame is starting...")
time.sleep(0.5)

#Main loop for the game
while True:

    if questions == len(questions_list): #If question bank is over then game is finished
        break

    time.sleep(2) 
    quiz() #Ask question
    questions += 1
    time.sleep(1)

    no_answers = True #variable to check no answers within the TIMEOUT limit
    first_player = True #variable to check the first player to press buzzer

    read, _, _ = select.select(sockets_list,[],[], TIMEOUT) #Checks any responses within the TIMEOUT limit

    for socket in read:
        message = receiveMsg(socket)
        if first_player and message != "false": #"false" is indication from the client that no response was given within 10 seconds 
            buzzer_player = socket #Player which pressed the buzzer first
            first_player = False
            no_answers = False
            break

    if no_answers:
        broadcast("No one pressed the buzzer!\n")
        time.sleep(0.5)
        broadcast("Proceeding to the next question...")
        continue
    else:
        for socket in sockets_list: #Broadcasting to other players to not press the buzzer
            if socket != buzzer_player and socket != s:
                sendMsg(f"\n{players[buzzer_player]} pressed the buzzer first..", socket)
                sendMsg(f"Please wait for {players[buzzer_player]} to answer", socket)

    sendMsg("Answer", buzzer_player) #Indicates the client to answer

    option = receiveMsg(buzzer_player) #Response from the player
    if option:
        game_over = checkAnswer(option, buzzer_player)
    else:
        game_over = checkAnswer("false", buzzer_player)

    scoreTable() #Displaying scores at the end of each question

    if game_over:
        break

#Game is finished
time.sleep(1)
broadcast("\nGame is over!!")

time.sleep(1)
if questions == len(questions_list):
    broadcast(f"Question bank is finished..")
else:
    broadcast(f"Winner is {max(scores_list, key = scores_list.get)}!!")

time.sleep(1)
broadcast("Hope you enjoyed playing the game!!\n")
broadcast("GameOver") #Indicates the client to close the connection
time.sleep(1)

s.close()