import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Day 3 Tasks")

# Clock for FPS control
clock = pygame.time.Clock()

# Circle setup
x, y = 300, 200
radius = 30
circle_color = (255, 0, 0)  # Red

# Line drawing variables
drawing = False
start_pos = None
lines = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- KEY PRESS EVENTS ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Press C to change circle color
                circle_color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

        # --- MOUSE EVENTS ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click starts line drawing
                drawing = True
                start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:  # Release mouse to finish line
                end_pos = event.pos
                lines.append((start_pos, end_pos))  # Save the line
                drawing = False

    # --- DRAWING AREA ---
    screen.fill((0, 0, 0))  # Clear screen (black)

    # Draw circle
    pygame.draw.circle(screen, circle_color, (x, y), radius)

    # Draw saved lines
    for line in lines:
        pygame.draw.line(screen, (255, 255, 255), line[0], line[1], 3)

    # Draw line while dragging (preview)
    if drawing:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (200, 200, 200), start_pos, current_pos, 2)

    # Update display
    pygame.display.flip()

    # Limit to 60 FPS
    clock.tick(60)

pygame.quit()



