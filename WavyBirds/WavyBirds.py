import sys, pygame
pygame.init()

size = width, height = 600, 400
speed = 0.01
white = 255, 255, 255
location = 0
screen = pygame.display.set_mode(size)

ball = pygame.image.load("vogel.png")
ballrect = ball.get_rect()
pipe = pygame.image.load("pijp.png")
piperect = pipe.get_rect()
piperect.bottom = height
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    print(speed)
    location += speed
    piperect = piperect.move(location - piperect.left, 0)
    if location > width:
        location = 0
    screen.fill(white)
    screen.blit(pipe, piperect)
    speed += .0001
    #ballrect = ballrect.move(speed)
    #if ballrect.left < 0 or ballrect.right > width:
    #    speed[0] = -speed[0]
    #if ballrect.top < 0 or ballrect.bottom > height:
    #    speed[1] = -speed[1]
    #screen.fill(white)
    #screen.blit(ball, ballrect)    
    pygame.display.flip()