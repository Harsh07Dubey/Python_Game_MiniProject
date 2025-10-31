import pygame
import sys

# Initialize pygame
pygame.init()

# Create a window (width=800, height=600)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game Window")

# Colors (R,G,B)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicks "X"
            pygame.quit()
            sys.exit()

    # Fill background color
    screen.fill(BLUE)

    # Update the screen
    pygame.display.flip()
