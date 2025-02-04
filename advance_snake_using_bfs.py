import pygame
import random
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 25
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 15

# Colors
BLACK = (0, 0, 0)      # Grid background
GREEN = (0, 255, 0)    # Snake
BROWN = (217, 187, 160)  # Brown apple (halve length)
BLUE = (0, 0, 255)     # Blue apple (double length)
RED = (255, 0, 0)      # Red apple (game over)
WHITE = (255, 255, 255)  # Grid lines

# Directions
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Advanced Snake Game with BFS")
clock = pygame.time.Clock()

# Font for game over text
font = pygame.font.Font(None, 36)

def draw_grid():
    """Draw the grid lines."""
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_SIZE))
        pygame.draw.line(screen, WHITE, (0, x), (SCREEN_SIZE, x))

def draw_cell(position, color):
    """Draw a single cell on the grid."""
    x, y = position
    rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def bfs_find_path(start, goal, obstacles):
    """Find the shortest path using BFS."""
    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)

            if (
                0 <= neighbor[0] < GRID_SIZE and
                0 <= neighbor[1] < GRID_SIZE and
                neighbor not in visited and
                neighbor not in obstacles
            ):
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # Reconstruct path
    path = []
    current = goal
    while current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

def generate_apple(snake, current_apple):
    """Generate an apple at a random location, avoiding the snake's body and current apple."""
    while True:
        apple_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if apple_position not in snake and apple_position != current_apple:
            return apple_position, random.choice([BROWN, BLUE, RED])

def main():
    # Initial snake setup
    snake = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]

    # Generate first apple
    apple, apple_color = generate_apple(snake, None)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Use BFS to find the shortest path to the apple
        path = bfs_find_path(snake[0], apple, set(snake))

        if path:
            new_head = path[0]
        else:
            # If no path is found, game over (snake is trapped)
            screen.fill(BLACK)
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, ((SCREEN_SIZE - game_over_text.get_width()) // 2, SCREEN_SIZE // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        # Check for collisions
        if (
            new_head in snake  # Snake touches itself
            or not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE)  # Snake hits the wall
            or (apple_color == RED and new_head == apple)  # Snake eats red apple
        ):
            # Game over
            screen.fill(BLACK)
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, ((SCREEN_SIZE - game_over_text.get_width()) // 2, SCREEN_SIZE // 2))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()

        # Move snake
        snake.insert(0, new_head)

        # Check if snake eats the apple
        if new_head == apple:
            if apple_color == BROWN:
                # Halve the snake length
                snake = snake[:max(1, len(snake) // 2)]
            elif apple_color == BLUE:
                # Double the snake length
                snake.pop()
                snake.extend(snake[-1:] * len(snake))

            # Generate a new apple
            apple, apple_color = generate_apple(snake, apple)
        else:
            # Remove tail if no apple eaten
            snake.pop()

        # Draw everything
        screen.fill(BLACK)

        # Draw the grid
        draw_grid()

        # Draw the snake
        for segment in snake:
            draw_cell(segment, GREEN)

        # Draw the apple
        draw_cell(apple, apple_color)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
