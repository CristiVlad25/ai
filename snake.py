#Credits to OpenAI and @vertinski for the prompt and for CODEX.

#Define a python function which is a classic snake game with a scoreboard.
#Display playing field using pygame library.

import pygame, sys, random, time

def gameOver():
    pygame.quit()
    sys.exit()

#Initialize pygame
pygame.init()

#Set the screen size
screen = pygame.display.set_mode((640,480))

#Set the window title
pygame.display.set_caption("Snake")

#Set up the colors
red = pygame.Color(255,0,0) #gameover
green = pygame.Color(0,255,0) #snake
black = pygame.Color(0,0,0) #score
white = pygame.Color(255,255,255) #background
brown = pygame.Color(165,42,42) #food

#Set up the font
font = pygame.font.SysFont('arial',48)

#Set up the fps
fpsController = pygame.time.Clock()

#Game variables
snakePos = [100,50]
snakeBody = [[100,50],[90,50],[80,50]]

foodPos = [random.randrange(1,63)*10,random.randrange(1,47)*10]
foodSpawn = True

direction = 'RIGHT'
changeto = direction

score = 0

#Game over function
def gameOver():
    myFont = pygame.font.SysFont('arial',72)
    GOsurf = myFont.render('Game Over!',True,red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320,15)
    screen.blit(GOsurf,GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()

def showScore(choice=1):
    sFont = pygame.font.SysFont('arial',24)
    Ssurf = sFont.render('Score : {0}'.format(score),True,black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80,10)
    else:
        Srect.midtop = (320,100)
    screen.blit(Ssurf,Srect)

#Main logic of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    #Validation of direction
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    #Update snake position [x,y]
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    #Snake body mechanism
    snakeBody.insert(0,list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    #Food Spawn
    if foodSpawn == False:
        foodPos = [random.randrange(1,63)*10,random.randrange(1,47)*10]
    foodSpawn = True

    #Background
    screen.fill(white)

    #Draw snake
    for pos in snakeBody:
        pygame.draw.rect(screen,green,pygame.Rect(pos[0],pos[1],10,10))

    #Draw food
    pygame.draw.rect(screen,brown,pygame.Rect(foodPos[0],foodPos[1],10,10))

    #Game Over conditions
    if snakePos[0] > 630 or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()

    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    #Common stuff
    showScore()
    pygame.display.flip()
    fpsController.tick(24)
