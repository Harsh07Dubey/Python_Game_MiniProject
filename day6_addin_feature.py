import pygame
import sys
import random
#import time

# Initialize pygame
pygame.init()

# Screen setup
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Day 6 - Power Up with Triangle")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Font
font = pygame.font.SysFont(None, 36)

# --- Function to reset the game ---
def reset_game():
    global x, y, score, rects, game_over, start_ticks, triangle, triangle_spawn_time, triangle_visible
    x, y = 100, 200
    score = 0
    rects = []
    for _ in range(50):  # spawn 5 rectangles
        rect_x = random.randint(50, width - 100)
        rect_y = random.randint(50, height - 100)
        rects.append(pygame.Rect(rect_x, rect_y, 60, 60))
    game_over = False
    start_ticks = pygame.time.get_ticks()  # record starting time

    # Power-up (triangle)
    triangle = None
    triangle_spawn_time = 0
    triangle_visible = False

# Timer setup (30 seconds)
time_limit = 30

# Initialize first game
reset_game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    reset_game()
                elif event.key == pygame.K_q:  # Quit
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

        # ---- Collision with rectangles ----
        for rect in rects:
            if rect.collidepoint(x, y):
                score += 1
                rects.remove(rect)
                break

        # ---- Power-up (Triangle) spawn logic ----
        current_time = pygame.time.get_ticks()

        # Spawn triangle every 5 seconds if not visible
        if not triangle_visible and current_time - triangle_spawn_time > 5000:
            tri_x = random.randint(50, width - 50)
            tri_y = random.randint(50, height - 50)
            triangle = [(tri_x, tri_y), (tri_x + 30, tri_y + 50), (tri_x - 30, tri_y + 50)]
            triangle_visible = True
            triangle_spawn_time = current_time

        # Hide triangle after 3 seconds if not collected
        if triangle_visible and current_time - triangle_spawn_time > 3000:
            triangle_visible = False

        # Collision with triangle
        if triangle_visible:
            tri_rect = pygame.Rect(min(p[0] for p in triangle), min(p[1] for p in triangle), 60, 60)
            if tri_rect.collidepoint(x, y):
                score += 10
                triangle_visible = False

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
        # Draw rectangles
        for rect in rects:
            pygame.draw.rect(screen, RED, rect)

        # Draw circle (player)
        pygame.draw.circle(screen, BLUE, (x, y), 25)

        # Draw triangle power-up
        if triangle_visible:
            pygame.draw.polygon(screen, YELLOW, triangle)

        # Draw Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw timer
        timer_text = font.render(f"Time: {remaining_time}", True, WHITE)
        screen.blit(timer_text, (width - 150, 10))

    else:
        # Show game over text
        over_text = font.render("GAME OVER!", True, GREEN)
        screen.blit(over_text, (width // 2 - 100, height // 2 - 20))

        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (width // 2 - 100, height // 2 + 20))

        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(restart_text, (width // 2 - 200, height // 2 + 60))

    # Update Screen
    pygame.display.flip()
    clock.tick(60)
