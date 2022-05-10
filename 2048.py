import random
import copy

#boardsize
boardsize=4

#This function prints the current board
def display():
  #find largest
  largest=board[0][0]
  for row in board:
    for element in row:
      if element>largest:
        largest=element

#set spaces
  numspaces=len(str(largest))

  for row in board:
        currRow='|'
        for element in row:
            #if current element is zero we add a space
            if element==0:
                currRow+=' '* numspaces +'|'
            #if not we add the value
            else:
                currRow+=(' '*(numspaces-len(str(element))))+str(element)+'|'
        print (currRow)
  print()


#merge one row left
def mergeOneRowL(row):
  #move everything as far to left as posible
  for j in range(boardsize-1):
     for i in range(boardsize-1,0,-1):
    #test if there is an empty space
        if row[i-1]==0:
          row[i-1]=row[i]
          row[i]=0
  for i in range(boardsize-1):
      if row[i]==row[i+1]:
        row[i]*=2
        row[i+1]=0
  for i in range(boardsize-1,0,-1):
        if row[i-1]==0:
          row[i-1]=row[i]
          row[i]=0

  return row

#This merges whole board to left
def merge_left(currentboard):
  for i in range(boardsize):
    currentboard[i]=mergeOneRowL(currentboard[i])
  return currentboard

#reverses the order of one row
def reverse(row):
  #add all element
  new=[]
  for i in range(boardsize-1,-1,-1):
    new.append(row[i])
  return new

#merges whole board to right
def merge_right(currentboard):
  for i in range(boardsize):
    currentboard[i]=reverse(currentboard[i])
    currentboard[i]=mergeOneRowL(currentboard[i])
    currentboard[i]=reverse(currentboard[i])
  return currentboard

#transpose the whole board
def transpose(currentboard):
  for j in range(boardsize):
    for i in range(j,boardsize):
      if not i==j:
        temp=currentboard[j][i]
        currentboard[j][i]=currentboard[i][j]
        currentboard[i][j]=temp
  return currentboard

#merges whole board up
def merge_up(currentboard):
  currentboard=transpose(currentboard)
  currentboard=merge_left(currentboard)
  currentboard=transpose(currentboard)

  return currentboard

#merges whole board down
def merge_down(currentboard):
  currentboard=transpose(currentboard)
  currentboard=merge_right(currentboard)
  currentboard=transpose(currentboard)

  return currentboard

#Picks a new value for theboard
def pickNewValue():
  if random.randint(1,8)==1:
    return 4
  else:
    return 2
#function to add value to the board
def addNewValue():
    rowNum=random.randint(0,boardsize-1)
    colNum=random.randint(0,boardsize-1)
    #Pick spots that are empty
    while not board[rowNum][colNum]==0:
        rowNum=random.randint(0,boardsize-1)
        colNum=random.randint(0,boardsize-1)
    #fill empty spot
    board[rowNum][colNum]=pickNewValue()

#whether user has won
def won():
    for row in board:
        if 2048 in row:
            return True
    return False


#whether user has lost
def noMoves():
    #create two copies of the board`
    tempboard1=copy.deepcopy(board)
    tempboard2=copy.deepcopy(board)

    #test every possible move
    tempboard1=merge_down(tempboard1)
    if tempboard1==tempboard2:
        tempboard1=merge_up(tempboard1)
        if tempboard1==tempboard2:
            tempboard1=merge_left(tempboard1)
            if tempboard1==tempboard2:
                tempboard1=merge_right(tempboard1)
                if tempboard1==tempboard2:
                    return True
    return False


#create a blank board
board=[]
for i in range(boardsize):
  row=[]
  for j in range(boardsize):
    row.append(0)
  board.append(row)


#fill two spots with random values
numNeeded=2
while numNeeded>0:
  rowNum=random.randint(0,boardsize-1)
  colNum=random.randint(0,boardsize-1)

  if board[rowNum][colNum]==0:
    board[rowNum][colNum]=pickNewValue()
    numNeeded-=1


print('Welcome to 2048!Your goal is to combine values to get the number 2048 by merging the board in different directions.Everytime, you will need to type\nd to merge right\nw to merge up\na to merge left\ns to merge down.\n\nHere is the starting board:')
display()

gameOver=False

# repeat asking the user for new moves while the game isn't over
while not gameOver:
  move=input("Which way do you want to merge?")
  validInput=True
  #create a copy of the board
  tempboard=copy.deepcopy(board)
  if move=='d':
    board=merge_right(board)
  elif move=='w':
    board=merge_up(board)
  elif move=='a':
    board=merge_left(board)
  elif move=='s':
    board=merge_down(board)
  else:
    validInput=False

  if not validInput:
    print('Your input was not valid, please try again')
  else:
      if board==tempboard:
          print('Try a different direction!')
      else:
          #test if user has won
          if won():
              display()
              print('You Won!')
              gameOver=True
          else:
              addNewValue()
              display()
              #check whether user lost
              if noMoves():
                  print('You have no more possible moves, you lose!')
                  gameOver=True
