import pygame
import sys
import random
import time

pygame.init()

pygame.mixer.init()

# --- Load Sounds ---
collision_sound = pygame.mixer.Sound("Sound_Effects/rect_coll.wav")
powerup_sound = pygame.mixer.Sound("Sound_Effects/power_up.wav")
gameover_sound = pygame.mixer.Sound("Sound_Effects/player_losing.wav")
completion_sound = pygame.mixer.Sound("Sound_Effects/game_completion.wav")
pygame.mixer.music.load("Sound_Effects/gamebacksound.wav")
pygame.mixer.music.play(-1)  # Loop background music


# Screen setup
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Day 8 - Interactive Buttons")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 100, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)

# Font
font = pygame.font.SysFont(None, 36)

# Game variables
x, y = 100, 200
score = 0
rects = []
game_state = "start"  # start, playing, paused, gameover
time_limit = 10
start_ticks = 0

# --- Helper Function to Reset Game ---
def reset_game():
    global x, y, score, rects, start_ticks, game_state
    x, y = 100, 200
    score = 0
    rects = []
    triangle_active = False
    triangle_timer = 0
    triangle_rect = pygame.Rect(0, 0, 40, 40)

    for _ in range(5):
        rect_x = random.randint(50, width - 100)
        rect_y = random.randint(50, height - 100)
        rects.append(pygame.Rect(rect_x, rect_y, 60, 60))
    start_ticks = pygame.time.get_ticks()
    game_state = "playing"
    pygame.mixer.music.load("Sound_Effects/gamebacksound.wav")
    pygame.mixer.music.play(-1)


# --- Button Drawing Function ---
def draw_button(text, rect, color, hover_color):
    mouse = pygame.mouse.get_pos()
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)

    label = font.render(text, True, WHITE)
    screen.blit(label, (rect.x + 10, rect.y + 8))

# --- Create Buttons ---
start_btn = pygame.Rect(width//2 - 60, height//2 - 30, 120, 50)
pause_btn = pygame.Rect(width - 120, 10, 100, 40)
resume_btn = pygame.Rect(width//2 - 60, height//2 - 30, 120, 50)
restart_btn = pygame.Rect(width//2 - 80, height//2 + 40, 160, 50)
quit_btn = pygame.Rect(width//2 - 80, height//2 + 100, 160, 50)

# --- Main Game Loop ---
while True:
    screen.fill(BLACK)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Start Screen ---
            if game_state == "start" and start_btn.collidepoint(event.pos):
                reset_game()

            # --- Playing State ---
            elif game_state == "playing" and pause_btn.collidepoint(event.pos):
                game_state = "paused"
                paused_time = pygame.time.get_ticks()

            # --- Paused State ---
            elif game_state == "paused":
                if resume_btn.collidepoint(event.pos):
                    start_ticks += pygame.time.get_ticks() - paused_time
                    game_state = "playing"

            # --- Game Over State ---
            elif game_state == "gameover":
                if restart_btn.collidepoint(event.pos):
                    reset_game()
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # --- Game States ---
    if game_state == "start":
        title = font.render("WELCOME TO THE GAME!", True, GREEN)
        screen.blit(title, (width//2 - 180, height//2 - 100))
        draw_button("START", start_btn, BLUE, LIGHT_BLUE)

    elif game_state == "playing":
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= 5
        if keys[pygame.K_RIGHT]: x += 5
        if keys[pygame.K_UP]: y -= 5
        if keys[pygame.K_DOWN]: y += 5

        # Boundary checks
        if x - 25 < 0: x = 25
        if x + 25 > width: x = width - 25
        if y - 25 < 0: y = width - 25
        if y + 25 > height: y = height - 25

        # Collision check
        for rect in rects:
            if rect.collidepoint(x, y):
                score += 1
                rects.remove(rect)
                powerup_sound.play()  # 🔊 play power-up sound
                break

        # Timer
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(time_limit - seconds_passed, 0)
        if remaining_time == 0 or len(rects) == 0:
            game_state = "gameover"
            if len(rects) == 0:
                completion_sound.play()  # 🔊 all rectangles collected
            else:
                gameover_sound.play()  # 🔊 time over


        # Draw game objects
        pygame.draw.circle(screen, BLUE, (x, y), 25)
        for rect in rects:
            pygame.draw.rect(screen, RED, rect)
        draw_button("PAUSE", pause_btn, GRAY, LIGHT_GRAY)

        # Score & Timer
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Time: {remaining_time}", True, WHITE), (10, 50))

    elif game_state == "paused":
        pause_text = font.render("GAME PAUSED", True, GREEN)
        screen.blit(pause_text, (width//2 - 100, height//2 - 100))
        draw_button("RESUME", resume_btn, BLUE, LIGHT_BLUE)

    elif game_state == "gameover":
        
        over_text = font.render("GAME OVER!", True, GREEN)
        screen.blit(over_text, (width//2 - 100, height//2 - 100))
        screen.blit(font.render(f"Final Score: {score}", True, WHITE), (width//2 - 100, height//2 - 50))
        pygame.mixer.music.stop()
        draw_button("RESTART", restart_btn, BLUE, LIGHT_BLUE)
        draw_button("QUIT", quit_btn, RED, LIGHT_RED)

    pygame.display.flip()
    clock.tick(60)
