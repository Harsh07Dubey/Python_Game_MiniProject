import pygame
import sys
import random

#initialize pygame
pygame.init()

# Screen Setup
width,height=600,400
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Day 5- Score & Multiple Objects")

clock = pygame.time.Clock()

# Colors
BLACK=(0,0,0)
BLUE=(0,0,255)
RED=(255,0,0)
GREEN=(0,255,0)
WHITE=(255,255,255)

# Circle setup
x,y=100,200
radius=25
speed=5

# Rectangle setup(random positions)
rects=[]
for _ in range(5): # 5 rectangle
    rect_x=random.randint(50,width-100)
    rect_y=random.randint(50,height-100)
    rects.append(pygame.Rect(rect_x,rect_y,60,60))

#Score
score=0
font=pygame.font.SysFont(None,36)

# Game state
game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    if not game_over:
        # Keyboard controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed

        # ---- Boundary check (stay inside window) ----
        if x - radius < 0:
            x = radius
        if x + radius > width:
            x = width - radius
        if y - radius < 0:
            y = radius
        if y + radius > height:
            y = height - radius

    
    

        # ---Collision check---
        for rect in rects:
            if rect.collidepoint(x,y): #If circle touches rectangle
                score+=1
                rects.remove(rect)# Remove rectangle after collision
                break

        if len(rects)==0:
            game_over=True

    #Clear Screen
    screen.fill(BLACK)

    if not game_over:
        # Draw rectangle
        for rect in rects:
            pygame.draw.rect(screen,RED,rect)

        #Draw circle
        circle_pos=(x,y)
        pygame.draw.circle(screen,BLUE,circle_pos,radius)


        #Draw score
        score_text=font.render(f"Score:{score}",True,WHITE)
        screen.blit(score_text,(10,10))
    else:
        #Show  Game Over Text
        over_text = font.render("GAME OVER!", True, GREEN)
        screen.blit(over_text, (width//2 - 100, height//2 - 20))

        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (width//2 - 120, height//2 + 20))

    #Update screen
    pygame.display.flip()
    clock.tick(60)