import sys, pygame
pygame.init()

speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode()

ball = pygame.image.load("images/intro_ball.gif")
ballori = ball
ballrect = ball.get_rect()
n = 0.0
giro = -1
while 1:
    n = n + giro * 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > screen.get_width():
        speed[0] = -speed[0]

    if ballrect.top < 0 or ballrect.bottom > screen.get_height():
        speed[1] = -speed[1]
        if speed[0] > 0 and ballrect.top < 0:
            giro = 1
        if speed[0] < 0 and ballrect.top < 0:
            giro = -1
        if speed[0] > 0 and ballrect.top > 0:
            giro = -1
        if speed[0] < 0 and ballrect.top > 0:
            giro = 1
    screen.fill(black)
    ball = pygame.transform.rotozoom(ballori,n , 1.0)
    screen.blit(ball, ballrect)
    pygame.display.flip()