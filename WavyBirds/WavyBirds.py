import math
import random
import sys
import pygame
from datetime import datetime, timedelta

pygame.init()
beachimg = pygame.image.load("strand.png")
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font('font.ttf', 32)

def gameover():
    text = font.render("Game Over!", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (width/2, height/2)
    screen.blit(text, textRect)
    pygame.display.flip()
    pygame.time.wait(2000)
    menu()  

def menu():
    game()

def game():
    gravity = 20
    pipegapsize = 300
    birdImg0 = pygame.transform.scale(pygame.image.load("bird_frame 0.gif"), (114, 63))
    birdImg1 = pygame.transform.scale(pygame.image.load("bird_frame 1.gif"), (114, 63))
    currentImg = birdImg0
    birdRect = currentImg.get_bounding_rect()

    birdRect.center = (width/2, height/3)
    birdRect.top = 0

    speed = 0.5
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
    while run:
        didbirdmove = False
        #beweging van de pijpen en de vogel
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    didbirdmove = True
                    birdspeed = -400
        


        flaptimeDist = -(prevFlapTime - datetime.now()).total_seconds()
        print (flaptimeDist)
        if flaptimeDist >= 1:
            print ("flap 1")
            currentImg = birdImg0
            birdRect = currentImg.get_bounding_rect()
            prevFlapTime = datetime.now()
        elif flaptimeDist >= 0.5:
            print ("flap 0")
            currentImg = birdImg1
            birdRect = currentImg.get_bounding_rect()


        if didbirdmove == False:
            birdspeed += gravity
        location += speed * deltatime.total_seconds()
        birdlocation += birdspeed * deltatime.total_seconds()

        toppipe = toppipe.move((width - location) - toppipe.left, 0)
        bottompipe = bottompipe.move((width - location) - bottompipe.left, 0)
        birdRect.center = (width/2, birdlocation)

        if location > width + toppipe.w:
            addedScore = False
            location = 0
            bottompipe.top = random.randint(pipegapsize + 10, height - 10)
            toppipe.bottom = bottompipe.top - pipegapsize 

        #renderen
        screen.blit(beachimg, (0, 0))
        screen.blit(currentImg, birdRect)
        screen.blit(toppipeimg, toppipe)
        screen.blit(bottompipeimg, bottompipe)

        #score text
        text = font.render(str(math.floor(score)), True, (0, 0, 0))
        textRect = text.get_rect()
        screen.blit(text, textRect)

        speed += deltatime.microseconds/100000
        pygame.display.flip()
        deltatime = datetime.now() - prevtime
        prevtime = datetime.now()

        #botsingen checken
        if birdRect.bottom > height:
            gameover()
            run = False

        if birdRect.bottom > height:
            run = False
            gameover()
            return

        if birdRect.colliderect(toppipe):
            run = False
            gameover()
            return
        if birdRect.colliderect(bottompipe):
            run = False
            gameover()
            return

        #score controleren
        if birdRect.left > bottompipe.right:
            if not addedScore:
                score += 0.5
                addedScore = True
        else:
            addedScore = False

menu()



    