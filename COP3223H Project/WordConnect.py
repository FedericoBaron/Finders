#Kristen Ng and Federico Baron
#Intro to C final project
#Word connect game (finders)


#i think the problem is we keep running the playgame function in the game loop because playinggame boolean is not global and it gets reset to false each time meaning it'll run it again

#imports libraries
import pygame
import random
import sys
import enchant
import math
import random
from random import shuffle


#initializes game
pygame.init()

#Define size of window
WIDTH = 500
HEIGHT = 700
 
#Define some colors
BACKGROUND = (178,206,255)
BLACK = (0, 0, 0)
BLOSSOM = (183, 255, 241)
YELLOW = (237,227,37)

#list of words
wordList = []

#play game bool
playingGame = False

#sets difficulty
difficulty = ""

#loads all letters to list
letter = []
for i in range(ord('A'),ord('Z')):
    letter.append(pygame.image.load(chr(i)+'.png'))


#list of letters
letterList = []

#temp letterlist
temp = []

#what the user inputs
userWord = ""

#list of coordinates
coordinatesX = []
coordinatesY = []

#makes a list with all "lastMove" as it keeps adding them to it
allMoves = []

#makes list with all the information needed to undo the previous move
lastMove = []

#Pre-Condition: takes in the text and the font to be used
#Post-Condition: returns the textSurface and rectangular text surface
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

#Pre-Condition: takes in the text, position of X, position of Y, and size
#Post-Condition: displays the text at the font in freesansbold font at the given size
def display_text(text, posX, posY, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    textSurf, textRect = text_objects(text, font)
    textRect.center = (posX,posY)
    screen.blit(textSurf, textRect)

#Pre-Condition: none
#Post-Condition: makes the easy, medium, and hard buttons
def makeButtons():
    #makes button shapes
    all_sprites.draw(screen)
    
    #adds text to button
    display_text(easy_button.get_name(), easy_button.get_posX(), easy_button.get_posY(), 20)
    display_text(medium_button.get_name(), medium_button.get_posX(), medium_button.get_posY(), 20)
    display_text(hard_button.get_name(), hard_button.get_posX(), hard_button.get_posY(), 20)
    
def buttonClick(posX, posY, centerX, centerY, width, height):
    if(centerX + width / 2 >= posX and centerX - width / 2 <= posX and centerY + height / 2 >= posY and centerY - height / 2 <= posY):
        print("Button clicked")
        return True
    return False
    
#Pre-Condition: takes in file with ranked dictionary word.
#Post-condtion: separates rank and word and passes it to make an object of the word class.
def processFile():

    #f is the file and it opens
    f = open("notsomanywordspart2.txt", "r")

    #defines rank and word
    word = []
    rank = []

    while True:
        
        #reads next line
        line = f.readline()

        #checks for EOF
        if(line == ""):
            break

        #Makes new word object with given rank and word
        #wordX = Word(line.split(" ")[0], line.split(" ")[8])
        wordX = line.split(" ")[8]
        #appends word object to wordList
        wordList.append(wordX)
        
    f.close()

#processess the file
processFile()

#Pre-Condition: takes in file with all words in dictionary
#Post-Condition: saves all words into list to be compared with user input
def checkIfWord(word):

    #checks if word from user is in dictionary
    d = enchant.Dict("en_US")

    #returns True or False
    return(d.check(word))

#Pre-Condition: It receives an unscrambled word string.
#Post-Condition: It returns a string of the scrambled word.
def scramble(word):
    print(word)
    word = list(word)
    shuffle(word)
    print(''.join(word))

    #adds each letter into letterList
    for i in range(0,len(word)):
        letterList.append(word[i])
        
    return ''.join(word)

#Pre-Condition:
#Post-Condition:
def plotLetter(x, y, word, size):
    print(ord(word)-97)
    drawLetter = Letter(x,y,letter[ord(word)-97],size)
    return drawLetter
    
    
#sets up board with given word
def setUp(word):

    #scrambles the word
    word = scramble(word)
    
    #initializes radius
    radius = 1
    
    #defines radius and lettersize based on the length of the word
    if(len(word) <8):
        radius = 140
    else:
        radius = 180

    angle = 360 / len(word)
    
    startAngle = 0

    i = 0
    while(startAngle < round(360,1)):
        
        #calculates position at angle
        y = round(math.sin(math.radians(startAngle)),6) * radius + HEIGHT / 2 
        x = round(math.cos(math.radians(startAngle)),6) * radius + WIDTH / 2 -30

        #plots a letter at the given location with the given dimensions
        plotLetter(x, y, word[i], 50)

        #appends to coordinate list
        coordinatesX.append(x)
        coordinatesY.append(y)
        
        #increases counter to do next letter
        i = i + 1

        #increases angle to do next location
        startAngle = startAngle + angle

#j allows the program to plot a letter in the right box
j = 0

#Pre-Condition: it starts when user clicks on word and while it remains clicked it keeps on adding the letters to form a word
#Post-Condition: it forms a word at the end and returns it
def connectWords():
    global userWord
    global j
    global lastMove
    global temp

    #if the user clicks
    if event.type == pygame.MOUSEBUTTONDOWN:

        #gets the position of where the user clicked
        clickPosX = pygame.mouse.get_pos()[0]
        clickPosY = pygame.mouse.get_pos()[1]

        #temporary letterlist to set letters that are clicked to -1 to indicate they have already been clicked and cannot be clicked again
        temp = letterList[:]
        
        #goes through every letter in the word that is diplayed and checks if it was clicked or not
        for i in range(0, len(coordinatesX)):

            #checks if the letter was already clicked and if the button is clicked
            if(temp[i]!= -1 and buttonClick(clickPosX-25, clickPosY-25, coordinatesX[i], coordinatesY[i], 50, 50)):

                #user word gets next letter
                userWord = userWord + temp[i]

                #appends everything that's needed for lastMove to be able to perform the undo function
                lastMove = []
                lastMove.append(temp[i])
                lastMove.append(coordinatesX[i])
                lastMove.append(coordinatesY[i])
                
                #letter is plotted in box grid
                letter = plotLetter(j*40,20,temp[i],40)
                all_sprites.add(letter)
                lastMove.append(letter)
                
                #last move is appended to all moves
                allMoves.append(lastMove)

                #j increases by one to do next box 
                j = j + 1

                #temp[i] is set to -1 to know that it was already used
                temp[i] = -1

                #shows that the button was clicked
                pygame.draw.rect(screen, YELLOW, [coordinatesX[i],coordinatesY[i],50,50], 10)

                #breaks out of loop
                break

        #debugging purposes        
        print(userWord)
        print(lastMove)
        print(allMoves)
        
    #checks if user word is the original word or a different word
    if (len(userWord) > 3 and checkIfWord(userWord)):
        print("yay")
        if (len(userWord) == len(letterList)):
            print("double yay")
            
    return

#Undos one move
def undo():

    #global variables needed to undo
    global lastMove
    global allMoves
    global userWord
    
    #shows that the button was clicked
    pygame.draw.rect(screen, BACKGROUND, [lastMove[1],lastMove[2],50,50], 10)

    #deletes last move
    if(len(allMoves)>0):
        del allMoves[len(allMoves)-1]
        if(len(allMoves)>0):
            lastMove = allMoves[len(allMoves)-1]
        else:
            lastMove = []

    #removes last letter from user word
    userWord = userWord[:-1]

    #sets last temp to what it used to be so it can be clicked again
    temp[len(temp)-1] = letterList[len(temp)-1]

    
    

#Draws boxes for plotting letters to form word
def drawBoxes():
    for i in range(0,len(letterList)):
        pygame.draw.rect(screen, BLACK, [i*40,20,40,40], 5)
    
    
#random word from text file
def getWord():
    return wordList[random.randint(0,len(wordList)-1)]

#Pre-Condition: word is a word from the list wordList[] and difficulty is whatever the user inputs.
#Post-Condition: returns a word of that difficulty level.
def difficultyWord(word, difficulty):
    
    #checks if word is too short or has non alpha characters. If one of those conditions is true, calls recursively to draw a new word
    if(len(word) <= 5  or not word.isalpha()):
        return difficultyWord(getWord(), difficulty)

    #checks if word is easy
    elif(len(word) < 8):
        if(difficulty == "easy"):
            return word
        else:
            return difficultyWord(getWord(), difficulty)

    #checks if word is medium
    elif(len(word) < 11):
        if(difficulty == "medium"):
            return word
        else:
            return difficultyWord(getWord(), difficulty)
        
    #else word is hard
    else:
        if(difficulty == "hard"):
            return word
        else:
            return difficultyWord(getWord(), difficulty)
       
#Pre-Condition: none
#Post-Condition: draws the entire home screen
def drawHomeScreen():

    # First, set the screen to light-blue.
    screen.fill(BACKGROUND)

    #import image of raccoon
    image = pygame.image.load('raccoonyay.png')
    
    #turns the image into the given scale
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    #displays image at given location
    screen.blit(image, (0, 0))
    
    #make buttons
    makeButtons()

#Pre-Condition: called from playGame()
#Post-Condition: changes screen to game screen
def gameScreen():

    #Sets background to color
    screen.fill(BACKGROUND)
    

def playGame():
    
    #sets screen to game screen
    gameScreen()

    #gets a word of the given difficulty
    word = difficultyWord(getWord(),difficulty)

    #sets up the screen for that word
    setUp(word)

    #draws boxes
    drawBoxes()

    #undo button
    all_sprites.remove(easy_button)
    all_sprites.remove(medium_button)
    all_sprites.remove(hard_button)
    all_sprites.add(undo_button)
    all_sprites.draw(screen)


#Creates image sprite
class Letter(pygame.sprite.Sprite):
    
    #construction for sprite, you can pass it posX, posY, and the image for that letter
    def  __init__(self, posX, posY, letter, size):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__letter = letter
        self.__posX = posX
        self.__posY = posY
        self.__size = size

        letter = pygame.transform.scale(letter, (size,size))
        screen.blit(letter,(posX,posY))

    #getter methods for name, posX, and posY
    def get_letter(self):
        return self.__letter
    
    def get_posX(self):
        return self.__posX
    
    def get_posY(self):
        return self.__posY




#Creates button sprite
class Button(pygame.sprite.Sprite):
    
    #construction for sprite, you can pass it more things like width and height
    def __init__(self, width, height, posX, posY, name, color):

        pygame.sprite.Sprite.__init__(self)

        #defines difficulty, posX, and posY in constructor
        self.__name = name
        self.__posX = posX
        self.__posY = posY
        
        #sets the size of the sprite
        self.image = pygame.Surface([width, height])

        #sets the color of the sprite
        self.image.fill(color)

        #the rectangle represents the dimensions of the sprite
        self.rect = self.image.get_rect()

        #sets the position of the sprite
        self.rect.center = (posX, posY)

    #getter methods for name, posX, and posY
    def get_name(self):
        return self.__name
    
    def get_posX(self):
        return self.__posX
    
    def get_posY(self):
        return self.__posY

#Open a new window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Finders")

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

#creates group of sprites
all_sprites = pygame.sprite.Group()

#creates easy, medium and hard buttons
easy_button = Button(100, 50, 100, HEIGHT -150, "easy", BLOSSOM)
medium_button = Button(100, 50, WIDTH / 2, HEIGHT -150, "medium", BLOSSOM)
hard_button = Button(100, 50, 400, HEIGHT -150, "hard", BLOSSOM)

#adds sprites to sprite group
all_sprites.add(easy_button)
all_sprites.add(medium_button)
all_sprites.add(hard_button)

#makes undo button
undo_button = Button(100, 50, 400, HEIGHT -50, "undo", YELLOW)
    
#draws the home screen
drawHomeScreen()

#processes the text file for rank and word
processFile()

# Main Program Loop
while carryOn:

    #keep loop running at the right speed
    clock.tick(60)
    
    # Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop


        #checks if user clicks button
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPosX = pygame.mouse.get_pos()[0]
            clickPosY = pygame.mouse.get_pos()[1]
            
            if(not playingGame and buttonClick(clickPosX, clickPosY, easy_button.get_posX(), easy_button.get_posY(), 100, 50)):
                playingGame = True
                difficulty = "easy"
                playGame()
            if(not playingGame and buttonClick(clickPosX, clickPosY, medium_button.get_posX(), medium_button.get_posY(), 100, 50)):
                playingGame = True
                difficulty = "medium"
                playGame()
            if(not playingGame and buttonClick(clickPosX, clickPosY, hard_button.get_posX(), hard_button.get_posY(), 100, 50)):
                playingGame = True
                difficulty = "hard"
                playGame()  
            if(playingGame and buttonClick(clickPosX, clickPosY, undo_button.get_posX(), undo_button.get_posY(),100, 50)):
                undo()
            elif(playingGame):
                connectWords()    
    
    #Update
    all_sprites.update()
    
    #Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
         
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
 

