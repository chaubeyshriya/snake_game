import pygame
import random

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 20  # Number of cells in each row and column
CELL_SIZE = 30  # Size of each cell in pixels
SCREEN_SIZE = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Static Snake and Food in One Line")

def place_food_1d_line(snake, grid_size):
    """Place food on the same row as the snake, but not on the snake."""
    snake_row = snake[0][0]
    while True:
        food_col = random.randint(0, grid_size - 1)
        if food_col != snake[0][1]:
            return snake_row, food_col

def draw_grid():
    """Draw the grid lines."""
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_SIZE))
        pygame.draw.line(screen, WHITE, (0, x), (SCREEN_SIZE, x))

def draw_snake(snake):
    """Draw the snake."""
    pygame.draw.rect(screen, GREEN, (snake[0][1] * CELL_SIZE, snake[0][0] * CELL_SIZE,CELL_SIZE, CELL_SIZE))

def draw_food(food):
    """Draw the food."""
    pygame.draw.rect(screen, RED, (food[1] * CELL_SIZE, food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Static snake and food setup
snake = [(5, 5)]  # Snake of size 1 at row 5, column 5
food = place_food_1d_line(snake, GRID_SIZE)

# Draw everything
running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_snake(snake)
    draw_food(food)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
