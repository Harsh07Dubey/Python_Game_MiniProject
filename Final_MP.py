import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# --- Load Sounds ---
collision_sound = pygame.mixer.Sound("Sound_Effects/rect_coll.wav")
powerup_sound = pygame.mixer.Sound("Sound_Effects/power_up.wav")
completion_sound = pygame.mixer.Sound("Sound_Effects/game_completion.wav")
player_lose = pygame.mixer.Sound("Sound_Effects/player_losing.wav")
pygame.mixer.music.load("Sound_Effects/gamebacksound.wav")
pygame.mixer.music.play(-1)  # Background music loop

# --- Screen Setup ---
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mini Game Project")

clock = pygame.time.Clock()

# --- Colors ---
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

# --- Font ---
font = pygame.font.SysFont(None, 36)

# Load background image
bg_image = pygame.image.load("background.png")
bg_image = pygame.transform.scale(bg_image, (width, height))


# --- Game Variables ---
x, y = 100, 200
radius = 25
score = 0
rects = []
game_state = "start"  # start, playing, paused, gameover
time_limit = 10
start_ticks = 0

# --- Power-Up Variables ---
triangle_active = False
triangle_timer = 0
triangle_rect = pygame.Rect(0, 0, 40, 40)

# --- Helper Function to Reset Game ---
def reset_game():
    global x, y, score, rects, start_ticks, game_state, triangle_active
    x, y = 100, 200
    score = 0
    rects = []
    for _ in range(5):
        rect_x = random.randint(50, width - 100)
        rect_y = random.randint(50, height - 100)
        rects.append(pygame.Rect(rect_x, rect_y, 60, 60))
    triangle_active = False
    start_ticks = pygame.time.get_ticks()
    game_state = "playing"

    # Restart background music when game restarts
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

# --- Buttons ---
start_btn = pygame.Rect(width//2 - 60, height//2 - 30, 120, 50)
pause_btn = pygame.Rect(width - 120, 10, 100, 40)
resume_btn = pygame.Rect(width//2 - 60, height//2 - 30, 120, 50)
restart_btn = pygame.Rect(width//2 - 80, height//2 + 40, 160, 50)
quit_btn = pygame.Rect(width//2 - 80, height//2 + 100, 160, 50)

# --- Main Loop ---
while True:
    screen.blit(bg_image, (0, 0))
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # --- Keyboard Shortcuts ---
        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                if event.key == pygame.K_p:  # Press 'P' to pause
                    game_state = "paused"
                    paused_time = pygame.time.get_ticks()

            elif game_state == "paused":
                if event.key == pygame.K_r:  # Press 'R' to resume
                    start_ticks += pygame.time.get_ticks() - paused_time
                    game_state = "playing"

            elif game_state == "gameover":
                if event.key == pygame.K_r:  # Press 'R' to restart
                    reset_game()
                elif event.key == pygame.K_q:  # Press 'Q' to quit
                    pygame.quit()
                    sys.exit()

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Start screen
            if game_state == "start" and start_btn.collidepoint(event.pos):
                reset_game()

            # Pause
            elif game_state == "playing" and pause_btn.collidepoint(event.pos):
                game_state = "paused"
                paused_time = pygame.time.get_ticks()

            # Resume
            elif game_state == "paused" and resume_btn.collidepoint(event.pos):
                start_ticks += pygame.time.get_ticks() - paused_time
                game_state = "playing"

                pygame.mixer.music.load("Sound_Effects/gamebacksound.wav")
                pygame.mixer.music.play(-1)

            # Game over screen
            elif game_state == "gameover":
                if restart_btn.collidepoint(event.pos):
                    reset_game()
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # --- Game States ---
    if game_state == "start":
        title = font.render("WELCOME TO THE GAME!", True, BLACK)
        screen.blit(title, (width//2 - 180, height//2 - 100))
        draw_button("START", start_btn, BLUE, LIGHT_BLUE)

    elif game_state == "playing":
        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= 5
        if keys[pygame.K_RIGHT]: x += 5
        if keys[pygame.K_UP]: y -= 5
        if keys[pygame.K_DOWN]: y += 5

        # Boundaries
        if x - radius < 0: x = radius
        if x + radius > width: x = width - radius
        if y - radius < 0: y = radius
        if y + radius > height: y = height - radius

        # Collision with Rectangles
        for rect in rects[:]:
            if rect.collidepoint(x, y):
                score += 1
                collision_sound.play()
                rects.remove(rect)

        # --- Power-Up Logic ---
        current_time = pygame.time.get_ticks()

        # Spawn triangle randomly
        if not triangle_active and random.randint(0, 500) == 0:
            triangle_rect.x = random.randint(50, width - 80)
            triangle_rect.y = random.randint(50, height - 80)
            triangle_active = True
            triangle_timer = current_time

        # Remove after 5 seconds
        if triangle_active and current_time - triangle_timer > 5000:
            triangle_active = False

        # Player collects triangle
        if triangle_active and triangle_rect.collidepoint(x, y):
            score += 10
            powerup_sound.play()
            triangle_active = False

        # Timer
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(time_limit - seconds_passed, 0)

        # --- DRAWING ---
        screen.blit(bg_image, (0, 0))  # Background image
        
        # End game
        if remaining_time == 0: #Time ran out = losing
            player_lose.play()
            pygame.mixer.music.stop()
            game_state = "gameover"

        elif len(rects) == 0:  # All rectangles collected = win
            completion_sound.play()
            pygame.mixer.music.stop()
            game_state = "gameover"

        # Draw Player
        pygame.draw.circle(screen, BLUE, (x, y), radius)

        # Draw Rectangles
        for rect in rects:
            pygame.draw.rect(screen, RED, rect)

        # Draw Triangle
        if triangle_active:
            pygame.draw.polygon(screen, GREEN, [
                (triangle_rect.centerx, triangle_rect.top),
                (triangle_rect.left, triangle_rect.bottom),
                (triangle_rect.right, triangle_rect.bottom)
            ])

        # UI
        draw_button("PAUSE", pause_btn, GRAY, LIGHT_GRAY)
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Time: {remaining_time}", True, BLACK), (10, 50))

    elif game_state == "paused":
        pygame.mixer.music.stop()
        pause_text = font.render("GAME PAUSED", True, BLACK)
        screen.blit(pause_text, (width//2 - 100, height//2 - 100))
        draw_button("RESUME", resume_btn, BLUE, LIGHT_BLUE)

    elif game_state == "gameover":
        # Display win or lose message
        if len(rects) == 0:  # Win condition
            over_text = font.render("YOU WIN!", True, BLACK)
        else:  # Lose condition
            over_text = font.render("YOU LOSE!", True, RED)

        # Draw text and buttons
        screen.blit(over_text, (width//2 - 100, height//2 - 100))
        screen.blit(font.render(f"Final Score: {score}", True, WHITE), (width//2 - 100, height//2 - 50))
        draw_button("RESTART", restart_btn, BLUE, LIGHT_BLUE)
        draw_button("QUIT", quit_btn, RED, LIGHT_RED)


    pygame.display.flip()
    clock.tick(60)