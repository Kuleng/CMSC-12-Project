import os
import time
COLSTART = '\033[92m'
COLEND = '\033[0m'
board = []
up = [-1,0]
down = [1,0]					#DIRECTIONS
left = [0,-1]
right = [0,1]
top_right = [-1,1]
bot_left = [1,-1]
top_left = [-1,-1]
bot_right = [1,1]
directions = [up,top_right,right,bot_right,down,bot_left,left,top_left]

def clear():
	os.system('cls||clear')

def setup_board_coor(height,width,maindat): #Sets up the board and its size
	i = 0
	while i < height:
		maindat.append([])
		i += 1
	total_height = height + 1
	total_width = width + 1
	for row in range(total_height):
		for col in range(total_width): # Ranges the setup size
			if (row != 0 and col!= 0):
				maindat[row-1].append("[_]") #appends the empty board to the list.
	return None
def setup_start_piece(maindat,boardsize):  #setups the 4 starting pieces in the middle of the board
	for row in range(len(maindat)):
		for col in range(len(maindat)):
			if (row == boardsize//2 and col == boardsize//2) or (row==boardsize//2-1 and col==boardsize//2-1):
				maindat[row][col] = "[B]" #sets black
			elif (row==boardsize//2-1 and col ==boardsize//2) or (row==boardsize//2 and col==boardsize//2-1):
				maindat[row][col] = "[W]" #sets white
def update_board(maindat): #Updates the board after evercol turn
	for row in range(len(maindat)+1):
		for col in range(len(maindat)+1): #Adds 1 for the coordinate-displacol
			if (row==0 and col == 0):
				print("  ",end="")
			elif row==0 and col != 0:
				print(col,end="  ")
			elif row != 0 and col == 0:
				print(row,end="")
			else:
				if maindat[row-1][col-1] == "[X]":
					print(COLSTART+"[_]"+COLEND,end="")
				else:
					print(maindat[row-1][col-1],end="")
		print()
def range_check(row,col): #checks if the coordinate entered is out of range
	if row == 0 or col == 0:
		print("Oops! You entered invalid coordinates!")
		return False
	else:
		return True
def turn_check(maindat,move_count): #returns the color of in-turn player
	if move_count % 2 == 0:
		return "[B]"
	elif move_count % 2 != 0:
		return "[W]"
def check_opponent(poss): #returns the color of the opponent
	if poss == "[W]":
		return "[B]"
	else:
		return "[W]"
def turn_validity(maindat,poss,oppo,row,col): #checks if the selected space is occupied
	if maindat[row-1][col-1] == poss: #Minus 1 because it starts at 0 
		return False 	#If you already occupied the space
	elif maindat[row-1][col-1] == oppo: #If the opponent already occupied the space
		return False
	else:
		maindat[row-1][col-1] = poss
		return True
def possible_moves(maindat,direction,poss,oppo): #Checks for possible moves and marks it as X
	move_list = []
	for row_var in range(len(maindat)): #loops for rows
		for col_var in range(len(maindat)): #loops for column
			if maindat[row_var][col_var] == poss: #selects a piece in possession of the current in-turn
				for dire in range(len(direction)): #loops for directions
					x = row_var
					y = col_var
					moveFlag = False #numbers of opponents looped
					for subloop in range(len(direction)): #subloop for each direction
						x += direction[dire][0] #first index for the direction
						y += direction[dire][1] #second index for the row/col
						if x < 0 or y < 0:
							break
						if x > len(maindat)-1 or y > len(maindat)-1: #breaks the loop if out of range based from the size of the board.
							break
						if maindat[x][y] == oppo:
							moveFlag = True
							continue
						elif maindat[x][y] == poss: #conditional for flipping the appended
							break
						elif maindat[x][y] == "[_]" and moveFlag == True: #Breaks the loop
							maindat[x][y] = "[X]" #marks the blank space as possible move
							move_list.append([x,y])
							break
						else:
							break
	return move_list
def flip_directions(maindat,direction,poss,oppo,row,col): #Creates a list for all opponents in a line that is ready to flip
	for dire in range(len(direction)): #loops for directions
		x = row -1
		y = col -1
		oppo_in_dir = []
		for a in range(len(direction)): #subloop for each direction
			x += direction[dire][0] #first index for the direction
			y += direction[dire][1] #second index for the row/col
			if x == -1 or y == -1: #TO AVOID INDECES TO BE -1 WHICH ACCESSES THE LAST INDEX OF A LIST.
				break
			if x > len(maindat)-1 or y > len(maindat)-1: #breaks the loop if out of range based from the size of the board.
				break
			if maindat[x][y] == oppo:
				oppo_in_dir.append([x,y]) #Append all the neighboring opponents in the direction
				continue
			elif maindat[x][y] == poss: #conditional for flipping the appended
				for b in range(len(oppo_in_dir)): #coordinates to the possession value
					maindat[oppo_in_dir[b][0]][oppo_in_dir[b][1]] = poss #Flips all the pieces on the list
				oppo_in_dir.clear()
				break
			elif maindat[x][y] == "[_]": #Breaks the loop
				break
			else:
				break
def x_check(maindat,row,col): #Checks if the selected coordinate has X (Which means the move is possible)
	if maindat[row-1][col-1] == "[X]":
		return True
	elif row > 8 or col > 8:
		print("Oops! You entered an impossible move.")
		return False
	else:
		print("Oops! You entered an invalid move.")
		return False
def point_counter(maindat): #Loops the board and adds points per W and B
	score = [0,0]
	for row in maindat:
		for box in row:
		 	if box == "[W]":
		 		score[0] += 1
		 	elif box == "[B]":
		 		score[1] += 1
	return score
def reset_move_list(maindat): #Resets the possible moves every other possessions.
	for row in range(len(maindat)):
		for col in range(len(maindat)):
			if maindat[row][col] =="[X]":
				maindat[row][col] = "[_]"
def possible_moves_counter(maindat): #Returns the number of possible moves or [X] in the board
	possiblemoves = 0 				#To determine if the turn is to pass or the game already ends
	for a in range(len(maindat)):
		for b in range(len(maindat)):
			if maindat[a][b] == "[X]":
				possiblemoves += 1
	return possiblemoves
def isFull(maindat): #Checks if the board is full
	blankspace = 0
	for row in range(len(maindat)):
		for col in range(len(maindat)):
			if maindat[row][col] == "[_]":
				blankspace += 1
	if blankspace == 0:
		return True # IF NO MORE BLANK SPACES, THE GAME ENDS
	else:
		return False
def pass_or_win(maindat,Xs,blanks): #If there are no more Xs, it's either a pass or the game is over.
	if Xs == 0 and blanks == False:
		return True
	elif Xs == 0 and blanks == True:
		return "GAME OVER"
	else:
		return False
def save_board(maindat): #Autosaves the current progress of the game
	act1 = open("othellodata.txt","w")
	for row in range(len(maindat)):
		for col in range(len(maindat)):
			act1.write(maindat[row][col]+" ")
		act1.write("\n")
	print("Autosave success.")
	act1.close()
def load_board(maindat): #Loads the last saved game
	try:
		act1 = open("othellodata.txt","r")
	except IOError:
		print("File not found!!")
		return False
	else:
		for line in act1:
			row_info = line[:-1]
			board_info = row_info.split(" ")
			maindat.append(board_info)
		print("You have Successfully loaded the last game progress!")
		act1.close()
	return True
print("==============WELCOME TO OTHELLO!!==============")
load_state = True #Defines initial load state value
while True:
	print("Please choose the size of the board:  ")
	print("[1] 8x8")
	print("[2] 6x6")
	print("[3] 4x4")
	print("[4] Continue/Load")
	print("[5] How to play")
	print("[6] Exit")
	choice = input("Enter your choice:  ")
	if choice == "6":
		break
	else:
		try:
			int(choice)
		except ValueError:
			clear()
			print("Invalid choice!!")
			continue
		else:
			choice = int(choice)
	if choice == 1:
		board_size = 8
		setup_board_coor(8,8,board)
	elif choice == 2:
		board_size = 6
		setup_board_coor(6,6,board)
	elif choice == 3:
		board_size = 4
		setup_board_coor(4,4,board)
	elif choice == 4 :
		load_state = load_board(board)
	elif choice == 5:
		clear()
		print("The black and white battle each other for victory. Conquer the opponent's piece by placing your piece on opponent piece's both ends!")
		print()
		print("You can only place your piece on coordinates with Xs because those are the only places where you can conquer an opponent's piece.")
		print()
		print("You cannot place your piece if it doesn't conquer other pieces, in rare cases where there are no possible moves, the turn automatically passes.")
		print()
		print("The highest scorer once the board is full is declared the winner of the game.")
		continue
	else:
		break

	if choice != 4: #If new game, setups the pieces.
		setup_start_piece(board,board_size)
	else:
		board_size = len(board) #If loaded, boardsize is assigned depending on how many lists are there in the main list.
		setup_start_piece(board,board_size)
	move_count = 1 #Initial counter for move count, to know who's in possession.
	time.sleep(1)
	clear()
	while True: #loops the game
		if load_state == False: #If there is no existing file to load, break and prompt if newgame or quit.
			break
		turn = turn_check(board,move_count) #Checks possession
		opponent = check_opponent(turn) #Checks opponent
		reset_move_list(board) #resets the Xs on the board, if there is/are any
		possible_moves(board,directions,turn,opponent) #sets the Xs on the board, based on the possession
		possible_moves_count = possible_moves_counter(board) #counts the Xs
		blankspaces = isFull(board) #counts the blank spaces (returns true or false)
		board_status = pass_or_win(board,possible_moves_count,blankspaces) #returns True if pass, GAME OVER if over.
		scores = point_counter(board) #Scores
		if move_count != 1:
			print("White's score:",scores[0]) #Display Scores after first move.
			print("Black's score:",scores[1])
		if board_status == True: #If boardstatus is true, pass.
			print("No moves available for",turn,". PASS.")
			move_count += 1
			continue
		elif board_status == "GAME OVER": #ENds game
			if scores[0] > scores[1]:
				print("GAME OVER! White wins with",scores[0],"points.")
			elif scores[0] == scores[1]:
				print("GAME OVER! Scores tied!")
			else:
				print("GAME OVER! Black wins with",scores[1],"points.")
			break
		else:
			update_board(board) #Updates board every move of a player
			save_board(board) #Auto save
			print("Enter 'q' if you want to quit")
			row_x = input("Enter the row of the space:  ")
			if row_x == "q" or row_x == "Q":
				break
			else:
				try:
					int(row_x)
				except ValueError:
					clear()
					print("The input is not an integer!!")
					continue
				else:
					row_x = int(row_x)
					if row_x > board_size:
						print("Oops! The row you entered is out of range!")
						continue
			col_y = input("Enter the column of the space:  ")
			if col_y == "q" or row_x == "Q":
				break
			else:
				try:
					int(col_y)
				except ValueError:
					clear()
					print("The input is not an integer!!")
					continue
				else:
					col_y = int(col_y)
					if col_y > board_size:
						print("Oops! THe column you entered is out of range!")
						continue
			clear()
			x_checker = x_check(board,row_x,col_y) #Checks if the coordinates is possible
			range_checker = range_check(row_x,col_y) #Checks if the coordinates is inside the board
			if range_checker == True and x_checker == True:
				valid = turn_validity(board,turn,opponent,row_x,col_y)
				flip_directions(board,directions,turn,opponent,row_x,col_y) #Flips the opponents, if there are any
				if valid == True:
					move_count += 1
	print("[1] NEW GAME")
	print("[2] QUIT")
	prompt2a = input("What do you want to do?  ")
	if prompt2a == "2":
		break
	else:
		try:
			int(prompt2a)
		except ValueError:
			board.clear()
			print("Invalid input! Game restarted.")
			continue
		else:
			prompt2a = int(prompt2a)
	if prompt2a == 1:
		board.clear()
		move_count = 1
		load_state = True
		continue
	else:
		board.clear()
		print("Invalid input! Game restarted.")