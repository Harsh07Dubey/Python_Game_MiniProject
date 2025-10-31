import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Day 7 - Background & Music")

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

# Load background image
bg_image = pygame.image.load("background.png")
bg_image = pygame.transform.scale(bg_image, (width, height))

# Load background music
pygame.mixer.music.load("Sound_Effects/gamebacksound.wav")
pygame.mixer.music.play(-1)  # Loop forever

# --- Function to reset the game ---
def reset_game():
    global x, y, score, rects, game_over, start_ticks, power_up, power_up_timer
    x, y = 100, 200
    score = 0
    rects = []
    for _ in range(5):  # spawn 5 rectangles
        rect_x = random.randint(50, width - 100)
        rect_y = random.randint(50, height - 100)
        rects.append(pygame.Rect(rect_x, rect_y, 60, 60))
    game_over = False
    start_ticks = pygame.time.get_ticks()
    power_up = None
    power_up_timer = 0

# Timer setup (10 sec)
time_limit = 10

# Game states
STATE_HOME = "home"
STATE_PLAYING = "playing"
STATE_PAUSE = "pause"
STATE_OVER = "over"
state = STATE_HOME

# Initialize first game
reset_game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == STATE_HOME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                state = STATE_PLAYING

        elif state == STATE_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    reset_game()
                    state = STATE_PLAYING
                elif event.key == pygame.K_h:  # Home
                    state = STATE_HOME
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

        elif state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                state = STATE_PAUSE

        elif state == STATE_PAUSE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume
                    state = STATE_PLAYING
                    start_ticks += pygame.time.get_ticks() - pause_start  # adjust timer
                elif event.key == pygame.K_r:
                    reset_game()
                    state = STATE_PLAYING
                elif event.key == pygame.K_h:
                    state = STATE_HOME
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    # --- GAME LOGIC ---
    if state == STATE_PLAYING and not game_over:
        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 5
        if keys[pygame.K_RIGHT]:
            x += 5
        if keys[pygame.K_UP]:
            y -= 5
        if keys[pygame.K_DOWN]:
            y += 5

        # Boundaries
        if x - 25 < 0: x = 25
        if x + 25 > width: x = width - 25
        if y - 25 < 0: y = 25
        if y + 25 > height: y = height - 25

        # Collisions with rectangles
        for rect in rects[:]:
            if rect.collidepoint(x, y):
                score += 1
                rects.remove(rect)

        # Timer
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = time_limit - seconds_passed
        if remaining_time <= 0 or len(rects) == 0:
            game_over = True
            state = STATE_OVER
            remaining_time = 0

    # --- DRAWING ---
    screen.blit(bg_image, (0, 0))  # Background image

    if state == STATE_HOME:
        title = font.render("WELCOME TO THE GAME", True, YELLOW)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(title, (width//2 - 150, height//2 - 50))
        screen.blit(start_text, (width//2 - 150, height//2))

    elif state == STATE_PLAYING:
        # Draw rectangles
        for rect in rects:
            pygame.draw.rect(screen, RED, rect)
        # Draw circle
        pygame.draw.circle(screen, BLUE, (x, y), 25)
        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        # Timer
        timer_text = font.render(f"Time: {remaining_time}", True, WHITE)
        screen.blit(timer_text, (width - 150, 10))

    elif state == STATE_PAUSE:
        pause_start = pygame.time.get_ticks()
        pause_text = font.render("PAUSED", True, YELLOW)
        resume_text = font.render("Press P to Resume", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        home_text = font.render("Press H for Home", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)
        screen.blit(pause_text, (width//2 - 50, height//2 - 60))
        screen.blit(resume_text, (width//2 - 100, height//2 - 20))
        screen.blit(restart_text, (width//2 - 100, height//2 + 20))
        screen.blit(home_text, (width//2 - 100, height//2 + 60))
        screen.blit(quit_text, (width//2 - 100, height//2 + 100))

    elif state == STATE_OVER:
        over_text = font.render("GAME OVER!", True, GREEN)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        home_text = font.render("Press H for Home", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)
        screen.blit(over_text, (width//2 - 100, height//2 - 60))
        screen.blit(score_text, (width//2 - 100, height//2 - 20))
        screen.blit(restart_text, (width//2 - 100, height//2 + 20))
        screen.blit(home_text, (width//2 - 100, height//2 + 60))
        screen.blit(quit_text, (width//2 - 100, height//2 + 100))

    pygame.display.flip()
    clock.tick(60)
