'''import pygame
import sys

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drawing Shapes in Pygame")

# Colors (R, G, B)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill background
    screen.fill(WHITE)

    # Draw shapes
    pygame.draw.rect(screen, RED, (100, 100, 200, 150))     # Rectangle
    pygame.draw.circle(screen, GREEN, (500, 300), 80)       # Circle
    pygame.draw.line(screen, BLUE, (50, 500), (750, 500), 5) # Line

    # Update screen
    pygame.display.flip()'''

#######################################################################


'''import pygame
import sys

pygame.init()

# Window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Circle")

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Circle starting position
x = 100
y = 100
radius = 30
speed_x = 3
speed_y = 2

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update circle position
    x += speed_x
    y += speed_y

    # Bounce on edges
    if x - radius <= 0 or x + radius >= 800:
        speed_x = -speed_x
    if y - radius <= 0 or y + radius >= 600:
        speed_y = -speed_y

    # Fill background
    screen.fill(BLUE)

    # Draw circle
    pygame.draw.circle(screen, WHITE, (x, y), radius)

    # Update display
    pygame.display.flip()

    # Control speed
    pygame.time.delay(10)'''

#########################################################

'''import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Circle Movement with Keys")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Circle properties
x, y = 400, 300   # Start at center
radius = 30
speed = 5         # Speed when pressing keys

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---- Keyboard Input ----
    keys = pygame.key.get_pressed()   # Check which keys are pressed

    if keys[pygame.K_LEFT]:   # Left arrow
        x -= speed
    if keys[pygame.K_RIGHT]:  # Right arrow
        x += speed
    if keys[pygame.K_UP]:     # Up arrow
        y -= speed
    if keys[pygame.K_DOWN]:   # Down arrow
        y += speed

    # ---- Drawing ----
    screen.fill(WHITE)                     # Clear screen
    pygame.draw.circle(screen, BLUE, (x, y), radius)  # Draw circle
    pygame.display.flip()                  # Update screen
    pygame.time.Clock().tick(60)        # 60 FPS'''


##################################################

'''import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Movement with Keys")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Circle properties
x, y = WIDTH // 2, HEIGHT // 2   # Start at center
radius = 30
speed = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---- Keyboard Input ----
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
    if x + radius > WIDTH:
        x = WIDTH - radius
    if y - radius < 0:
        y = radius
    if y + radius > HEIGHT:
        y = HEIGHT - radius

    # ---- Drawing ----
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (x, y), radius)
    pygame.display.flip()
    pygame.time.Clock().tick(60)'''



