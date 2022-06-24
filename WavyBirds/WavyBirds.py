import math
import random
import sys
import pygame
import shelve
from datetime import datetime, timedelta

def gameover(score):
    WriteScore(score)
    font = pygame.font.Font('font.ttf', 40)
    text = font.render("Game Over!", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (width/2, height/2 - 60)
    screen.blit(text, textRect)
    rectbottom = textRect.bottom

    font = pygame.font.Font('font.ttf', 20)
    text = font.render("[ESC]: Home", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width/2, 0)
    textRect.top = rectbottom
    screen.blit(text, textRect)
    rectbottom = textRect.bottom

    text = font.render("[Space]: Retry", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width/2, 0)
    textRect.top = rectbottom
    screen.blit(text, textRect)
    pygame.display.flip()
    leave = False

    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                    leave = True
                elif event.key == pygame.K_SPACE:
                    game()
                    leave = True

def WriteScore(score):
    d = shelve.open("Score")
    try:
        if float(d.get("highscore")) < math.floor(score):
            d["highscore"] = math.floor(score)
    except:
        d["highscore"] = math.floor(score)
        print ("Error write")
    d.close()

def ReadScore():
    try:
        d = shelve.open("score")
        ret = d["highscore"]
        d.close()
        return ret
    except:
        print ("Error read")
        return 0

def menu():
    screenCenterX = width/2
    screenCenterY = height/2
    screen.blit(beachimg, (0, 0))
    font = pygame.font.Font('font.ttf', 50)
    buttonRect = pygame.draw.circle(screen, (200, 20, 20), (screenCenterX, screenCenterY), 40)
    pygame.draw.polygon(screen, (20, 150, 200), [( screenCenterX + 30, screenCenterY), ( screenCenterX - 18, screenCenterY +  28), ( screenCenterX -  18, screenCenterY -  28)])
    text = font.render("Wavy Seagulls", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (width/2, height/2 - 100)
    screen.blit(text, textRect)
    pygame.display.flip()
    clicked = False

    while not clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if buttonRect.collidepoint(event.pos):
                        clicked = True
    game()  

def game():
    highscore = ReadScore()
    gravity = 25
    pipegapsize = 200
    birdImg0 = pygame.transform.scale(pygame.image.load("bird_frame 0.gif"), (114, 63))
    birdImg1 = pygame.transform.scale(pygame.image.load("bird_frame 1.gif"), (114, 63))
    currentImg = birdImg0
    birdRect = currentImg.get_bounding_rect()
    clock = pygame.time.Clock()
    font = pygame.font.Font('font.ttf', 32)

    birdRect.center = (width/2, height/3)
    birdRect.top = 0

    birds = [ birdRect, birdRect.copy(), birdRect.copy() ]

    speed = 1
    location = 0
    birdlocation = 0
    birdspeed = 0
    toppipeimg = pygame.image.load("paal.png")
    bottompipeimg = pygame.image.load("paal.png")
    bottompipe = bottompipeimg.get_bounding_rect(1)
    toppipe = toppipeimg.get_rect()
    bottompipe.top = random.randint(pipegapsize + 10, height - 10)
    toppipe.bottom = bottompipe.top - pipegapsize

    toppipe.left = width
    bottompipe.left = width
    prevtime = datetime.now()
    prevFlapTime = datetime.now()
    run = True
    deltatime = timedelta(0)
    score = 0.5
    addedScore = False
    addedBird = False
    while run:
        clock.tick(30)
        didbirdmove = False
        #beweging van de pijpen en de vogel
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    didbirdmove = True
                    birdspeed = -400
                if event.key == pygame.K_ESCAPE:
                    menu()

        flaptimeDist = -(prevFlapTime - datetime.now()).total_seconds()
        if flaptimeDist >= 1:
            currentImg = birdImg0
            prevFlapTime = datetime.now()
        elif flaptimeDist >= 0.5:
            currentImg = birdImg1

        if didbirdmove == False:
            birdspeed += gravity
        location += speed * deltatime.total_seconds()

        birdlocation += birdspeed * deltatime.total_seconds()

        toppipe = toppipe.move((width - location) - toppipe.left, 0)
        bottompipe = bottompipe.move((width - location) - bottompipe.left, 0)
        updatepositions(birds, birdlocation)

        if location > width + toppipe.w:
            addedScore = False
            location = 0
            bottompipe.top = random.randint(pipegapsize + 10, height - 10)
            toppipe.bottom = bottompipe.top - pipegapsize 

        #renderen
        screen.blit(beachimg, (0, 0))
        for bird in birds:
            screen.blit(currentImg, bird)
        screen.blit(toppipeimg, toppipe)
        screen.blit(bottompipeimg, bottompipe)

        #score text
        text = font.render(str(math.floor(score)) + "  HIGH: " + str(highscore), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, textRect)

        speed += deltatime.microseconds/100000
        pygame.display.flip()
        deltatime = datetime.now() - prevtime
        prevtime = datetime.now()

        #botsingen checken
        if birdRect.bottom > height:
            run = False
        for bird in birds:
            if bird.colliderect(toppipe) or bird.colliderect(bottompipe):
                if (len(birds) < 2):
                    run = False
                else:
                    birds.pop()
                    location += len(birds) * (bird.w + 25)

        if birdRect.left > bottompipe.right:
            if not addedScore:
                score += 0.5
                addedScore = True
        else:
            addedScore = False
        if score % 5 == 0:
            if not addedBird:
                addedBird = True
                birds.append(birdRect.copy())
        else:
            addedBird = False
    gameover(score)

def updatepositions(birds, firstpos):
    for i in range(0, len(birds)):
        bird = birds[i]
        if (i == 0):
            bird.center = (width/2 - (i * bird.w + 25), firstpos)
        else:
            ypos = bird.center[1]
            bird.center = (width/2 - (i * bird.w + 25), ypos + ((birds[i - 1].center[1] - ypos)/4))
        birds[i] = bird
    return birds

pygame.init()
beachimg = pygame.image.load("strand.png")
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Wavy Seagulls")

menu()



    