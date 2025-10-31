import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Day 6 - Restart & Quit")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont(None, 36)

# --- Function to reset the game ---
def reset_game():
    global x,y,score,rects,game_over,start_ticks
    x,y=100,200
    score=0
    rects=[]
    for _ in range(5): #spawn  5 rectangles
        rect_x = random.randint(50, width - 100)
        rect_y = random.randint(50, height - 100)
        rects.append(pygame.Rect(rect_x, rect_y, 60, 60))
    game_over = False
    start_ticks = pygame.time.get_ticks()  # record starting time

# Timer setup(10 second)
time_limit=10

# Initialize first game
reset_game()

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r: # Restart
                    reset_game()
                elif event.key==pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

    if not game_over:
        # Keyboard controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 5
        if keys[pygame.K_RIGHT]:
            x += 5
        if keys[pygame.K_UP]:
            y -= 5
        if keys[pygame.K_DOWN]:
            y += 5

        
        # ---- Boundary check ----
        if x - 25 < 0: x = 25
        if x + 25 > width: x = width - 25
        if y - 25 < 0: y = 25
        if y + 25 > height: y = height - 25


        # ---- Collision check ----
        for rect in rects:
            if rect.collidepoint(x, y):
                score += 1
                rects.remove(rect)
                break

        # If all rectangles collected → Game Over
        if len(rects) == 0:
            game_over = True

        # ---- Timer check ----
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = time_limit - seconds_passed
        if remaining_time <= 0:
            game_over = True
            remaining_time = 0

    # Clear screen
    screen.fill(BLACK)

    if not game_over:
        #Draw rectangle
        for rect in rects:
            pygame.draw.rect(screen,RED,rect)
    
        # Draw circle
        pygame.draw.circle(screen,BLUE,(x,y),25)

        #Draw Score
        score_text=font.render(f"Score: {score}",True,WHITE)
        screen.blit(score_text,(10,10))

        # Draw timer
        timer_text = font.render(f"Time: {remaining_time}", True, WHITE)
        screen.blit(timer_text, (width - 150, 10))

        
    else:
        # Show game over text
        over_text=font.render("GAME OVER!",True,GREEN)
        screen.blit(over_text,(width//2-100,height//2-20))

        score_text=font.render(f"Final Score: {score}",True,WHITE)
        screen.blit(score_text,(width//2-100,height//2+20))

        restart_text=font.render("Press R to Restart or Q to Quit",True,WHITE)
        screen.blit(restart_text,(width//2-200,height//2+60))

    # Update Screen
    pygame.display.flip()
    clock.tick(60)
