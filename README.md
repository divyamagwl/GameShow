<h1 align="center">Game Show</h1>
<p>
</p>

> This repository contains the implementation of multiplayer General Knowledge Game Show. Socket programming in Python3 have been used to implement it. Number of players are set to 3 currently.

## Rules of the Game show

You have 10 seconds to press buzzer (enter any letter or number on the keyboard).

The first one to press buzzer will be given the opportunity to answer

You have 10 seconds to answer if your answer is correct you get +1 , in all other cases -0.5

First one to reach 5 points will be declared as the winner

## Major modules used 

	select 
	socket
	termios

## Instruction to run the project
Clone the repo and execute the following command on different terminals

	python3 server.py (1 terminal)
	python3 client.py (3 different terminals)

## Some features of this project

Currently the number of players has been set to 3 but you can change it in the server code easily. 
Similarly the maximum score to finish the game could be changed in the server code.

The project has functions to shuffle the questions and even order of the options each time you try to play the game again.

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br/>Feel free to check [issues page](https://github.com/divyamagwl/GameShow/issues).

## Show your support

Give a ⭐️ if this project helped you!

