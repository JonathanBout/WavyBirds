import random
import pygame
from datetime import datetime, timedelta

def gameover():
    print("Game over!")
    pygame.time.wait(1000)
    menu()

def game() :
    background = 75, 75, 250
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    gravity = 20
    pipegapsize = 125

    birdrect = pygame.Rect(width/2-20, 0, 40, 40)
    birdrect.top = 0
    pygame.init()

    speed = 0.05
    location = 0
    birdlocation = 0
    birdspeed = 0
    toppipe = pygame.Rect(0, 0, 20, 0)
    bottompipe = pygame.Rect(0, 0, 20, random.randint(10, height - pipegapsize + 10))

    bottompipe.bottom = height
    toppipe.h = 1600
    toppipe.bottom = bottompipe.top - pipegapsize

    toppipe.left = width
    bottompipe.left = width
    prevtime = datetime.now()
    run = True
    deltatime = timedelta(0)
    while run:
        didbirdmove = False
        #beweging van de pijpen en de vogel
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    didbirdmove = True
                    birdspeed = -400
        if didbirdmove == False:
            birdspeed += gravity
            
        location += speed * deltatime.total_seconds()
        birdlocation += birdspeed * deltatime.total_seconds()

        toppipe = toppipe.move((width - location) - toppipe.left, 0)
        bottompipe = bottompipe.move((width - location) - bottompipe.left, 0)
        birdrect = birdrect.move(0, birdlocation - birdrect.top)

        if location > width + toppipe.w:
            location = 0
            bottompipe.h = random.randint(10, height - pipegapsize + 10)
            bottompipe.bottom = height
            toppipe.bottom = bottompipe.top - pipegapsize 



        #renderen
        bg = pygame.image.load("strand.png")
        screen.blit(bg, (0, 0))
        #screen.fill(background);
        pygame.draw.rect(screen, (100, 100, 100), birdrect)
        pygame.draw.rect(screen, (255, 100, 50), toppipe)
        pygame.draw.rect(screen, (255, 100, 50), bottompipe)
        speed += deltatime.microseconds/100000
        pygame.display.flip()
        deltatime = datetime.now() - prevtime
        prevtime = datetime.now()

        #botsingen checken
        if birdrect.bottom > height:
            gameover()
            run = False

        if birdrect.colliderect(toppipe):
            run = False
            gameover()
        if birdrect.colliderect(bottompipe):
            run = False
            gameover()

def menu():
    game()

menu()
    