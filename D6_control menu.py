import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Day 6 - Full Game with Pause/Home/Power-Up")

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

# Game states
STATE_HOME = "home"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"

state = STATE_HOME

# Timer setup
time_limit = 10
start_ticks = 0
pause_start = 0
pause_duration = 0

# Player & game variables
x, y = 100, 200
score = 0
rects = []
power_up = None
power_up_spawn_time = 0


# --- Function to reset the game ---
def reset_game():
    global x, y, score, rects, game_over, start_ticks, pause_duration, power_up
    x, y = 100, 200
    score = 0
    rects = []
    for _ in range(5):  # spawn 5 rectangles
        rect_x = random.randint(50, width - 100)
        rect_y = random.randint(50, height - 100)
        rects.append(pygame.Rect(rect_x, rect_y, 60, 60))
    game_over = False
    start_ticks = pygame.time.get_ticks()
    pause_duration = 0
    power_up = None


# --- Spawn a power-up triangle ---
def spawn_power_up():
    global power_up, power_up_spawn_time
    tri_x = random.randint(50, width - 50)
    tri_y = random.randint(50, height - 50)
    power_up = pygame.Rect(tri_x, tri_y, 40, 40)
    power_up_spawn_time = pygame.time.get_ticks()


# --- Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle events by state
        if state == STATE_HOME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                reset_game()
                state = STATE_PLAYING

        elif state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause
                    state = STATE_PAUSED
                    pause_start = pygame.time.get_ticks()

        elif state == STATE_PAUSED:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume
                    pause_duration += pygame.time.get_ticks() - pause_start
                    state = STATE_PLAYING
                elif event.key == pygame.K_h:  # Home
                    state = STATE_HOME
                elif event.key == pygame.K_r:  # Restart
                    reset_game()
                    state = STATE_PLAYING

        elif state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    reset_game()
                    state = STATE_PLAYING
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_h:  # Home
                    state = STATE_HOME

    # -------------------- GAME LOGIC --------------------
    if state == STATE_PLAYING:
        # Movement
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

        # Collision with rectangles
        for rect in rects:
            if rect.collidepoint(x, y):
                score += 1
                rects.remove(rect)
                break

        # Collision with power-up
        if power_up and power_up.collidepoint(x, y):
            score += 10
            power_up = None

        # Power-up disappears after 3 sec
        if power_up and pygame.time.get_ticks() - power_up_spawn_time > 3000:
            power_up = None

        # Randomly spawn power-up
        if not power_up and random.randint(1, 200) == 1:
            spawn_power_up()

        # Timer check (adjusted for pause)
        seconds_passed = (pygame.time.get_ticks() - start_ticks - pause_duration) // 1000
        remaining_time = time_limit - seconds_passed
        if remaining_time <= 0 or len(rects) == 0:
            state = STATE_GAME_OVER
            remaining_time = 0

    # -------------------- DRAW --------------------
    screen.fill(BLACK)

    if state == STATE_HOME:
        title = font.render("Welcome to the Game!", True, YELLOW)
        screen.blit(title, (width // 2 - 150, height // 2 - 40))
        start_text = font.render("Press S to Start", True, WHITE)
        screen.blit(start_text, (width // 2 - 100, height // 2 + 10))

    elif state == STATE_PLAYING:
        # Rectangles
        for rect in rects:
            pygame.draw.rect(screen, RED, rect)

        # Circle (player)
        pygame.draw.circle(screen, BLUE, (x, y), 25)

        # Power-up (triangle)
        if power_up:
            pygame.draw.polygon(screen, GREEN,
                                [(power_up.x, power_up.y + 40),
                                 (power_up.x + 20, power_up.y),
                                 (power_up.x + 40, power_up.y + 40)])

        # Score & Timer
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        timer_text = font.render(f"Time: {remaining_time}", True, WHITE)
        screen.blit(timer_text, (width - 150, 10))

    elif state == STATE_PAUSED:
        pause_text = font.render("PAUSED", True, GREEN)
        screen.blit(pause_text, (width // 2 - 60, height // 2 - 20))
        info = font.render("Press P=Resume, R=Restart, H=Home", True, WHITE)
        screen.blit(info, (width // 2 - 200, height // 2 + 20))

    elif state == STATE_GAME_OVER:
        over_text = font.render("GAME OVER!", True, GREEN)
        screen.blit(over_text, (width // 2 - 100, height // 2 - 40))
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (width // 2 - 100, height // 2))
        restart_text = font.render("Press R=Restart, H=Home, Q=Quit", True, WHITE)
        screen.blit(restart_text, (width // 2 - 220, height // 2 + 40))

    pygame.display.flip()
    clock.tick(60)
