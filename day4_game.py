# Circle - Rectangle Collision

import pygame
import sys

# initialize pygame
pygame.init()

# Screen setup
width,Height=600,400
screen=pygame.display.set_mode((width,Height))
pygame.display.set_caption("Day 4 - Collision Detection")

clock=pygame.time.Clock()

# Colors

Black=(0,0,0)
Blue=(0,0,225)
RED=(255,0,0)
Green=(0,225,0)

# Circle setup
x,y=100,200
radius=25
speed=5

#rectangle setup
rect = pygame.Rect(300,150,100,100) # (x, y, width, height)

# Game loop
while  True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Keyboard controls
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
           x-=speed
    if keys[pygame.K_RIGHT]:
           x+=speed
    if keys[pygame.K_UP]:
           y-=speed
    if keys[pygame.K_DOWN]:
           y+=speed

    
    
    # ---- Boundary check (stay inside window) ----
    if x - radius < 0:
        x = radius
    if x + radius > width:
        x = width - radius
    if y - radius < 0:
        y = radius
    if y + radius > Height:
        y = Height - radius



    # clear screen
    screen.fill(Black)

    # Draw rectangle
    pygame.draw.rect(screen,RED,rect)

    # Draw circle
    circle_pos = (x, y)
    pygame.draw.circle(screen, Blue, circle_pos, radius)

    # ---- Collision check ----
    if  rect.collidepoint(x,y): # If circle centre is inside rectangle
            pygame.draw.circle(screen,Green,circle_pos,radius) #change circle color

    # update scrreen
    pygame.display.flip()
    clock.tick(60)
    
    #pygame.time.Clock().tick(60)
