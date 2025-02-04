import pygame
import sys
from collections import deque
import random

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 20  # Number of cells in each row and column
CELL_SIZE = 30  # Size of each cell in pixels
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 10  # Frames per second

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Snake Game with DFS")

# Directions: Right, Left, Down, Up
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def is_valid(x, y, snake, grid_size):
    """Check if a position is within the grid and not part of the snake."""
    return 0 <= x < grid_size and 0 <= y < grid_size and (x, y) not in snake

def dfs(snake_head, food, snake_body, grid_size):
    """Find a path from snake head to food using DFS."""
    stack = [snake_head]
    visited = set()
    visited.add(snake_head)
    parent = {snake_head: None}

    while stack:
        current = stack.pop()

        if current == food:
            # Reconstruct path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            if next_pos not in visited and is_valid(next_pos[0], next_pos[1], snake_body, grid_size):
                stack.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current

    return None  # No path found

def place_food(snake_body, grid_size):
    """Place food at a random position that is not occupied by the snake."""
    while True:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if (x, y) not in snake_body:
            return x, y

def draw_grid():
    """Draw the grid lines."""
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_SIZE))
        pygame.draw.line(screen, WHITE, (0, x), (SCREEN_SIZE, x))

def draw_snake(snake):
    """Draw the snake."""
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    """Draw the food."""
    pygame.draw.rect(screen, RED, (food[1] * CELL_SIZE, food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    clock = pygame.time.Clock()

    # Initialize snake and food
    snake = deque([(0, 0)])  # Snake starts at the top-left corner
    food = place_food(snake, GRID_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Use DFS to find a path to food
        path = dfs(snake[0], food, snake, GRID_SIZE)

        if not path or len(path) < 2:
            print("Game Over! No valid moves.")
            running = False
            continue

        # Move the snake
        next_pos = path[1]
        snake.appendleft(next_pos)

        if next_pos == food:
            food = place_food(snake, GRID_SIZE)  # Place new food
        else:
            snake.pop()  # Remove tail

        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
