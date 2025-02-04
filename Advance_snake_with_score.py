import pygame
import random
import sys
from collections import deque

# Constants
GRID_SIZE = 25
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 15

# Colors
BLACK = (0, 0, 0)  # Grid background
GREEN = (0, 255, 0)  # Snake
BROWN = (217, 187, 160)  # Brown apple (halve length)
BLUE = (0, 0, 255)  # Blue apple (double length)
RED = (255, 0, 0)  # Red apple (game over)
WHITE = (255, 255, 255)  # Game over screen
YELLOW = (255, 255, 0)  # Grid lines
TEXT_COLOR = (0, 0, 0)  # Score text

# Directions
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Autonomous Snake Game")
clock = pygame.time.Clock()
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

def generate_apple(snake, current_apple):
    """Generate an apple at a random location, avoiding the snake's body and current apple."""
    while True:
        apple_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if apple_position not in snake and apple_position != current_apple:
            return apple_position, random.choice([BROWN, BLUE, RED])

def bfs_path(start, target, obstacles):
    """Perform BFS to find the shortest path from start to target, avoiding obstacles."""
    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                0 <= neighbor[0] < GRID_SIZE
                and 0 <= neighbor[1] < GRID_SIZE
                and neighbor not in visited
                and neighbor not in obstacles
            ):
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None  # No path found

def main():
    # Initial setup
    snake = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
    apple, apple_color = generate_apple(snake, None)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Find path to the apple using BFS
        path_to_apple = bfs_path(snake[0], apple, set(snake[1:]))

        if path_to_apple:
            # Follow the path to the apple
            new_head = path_to_apple[0]
        else:
            # If no path, make a random valid move
            valid_moves = [
                (snake[0][0] + dx, snake[0][1] + dy)
                for dx, dy in DIRECTIONS
                if 0 <= snake[0][0] + dx < GRID_SIZE
                and 0 <= snake[0][1] + dy < GRID_SIZE
                and (snake[0][0] + dx, snake[0][1] + dy) not in snake
            ]
            if valid_moves:
                new_head = random.choice(valid_moves)
            else:
                # No valid moves, game over
                running = False
                break

        # Check for collisions
        if (
            new_head in snake  # Snake touches itself
            or not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE)  # Snake hits the wall
            or (apple_color == RED and new_head == apple)  # Snake eats red apple
        ):
            # Game over
            screen.fill(WHITE)
            game_over_text = font.render(f"Game Over! Score: {score}", True, TEXT_COLOR)
            screen.blit(game_over_text, ((SCREEN_SIZE - game_over_text.get_width()) // 2, SCREEN_SIZE // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        # Move the snake
        snake.insert(0, new_head)

        # Check if the snake eats the apple
        if new_head == apple:
            if apple_color == BROWN:
                # Halve the snake length
                snake = snake[:max(1, len(snake) // 2)]
                score += 1
            elif apple_color == BLUE:
                # Double the snake length
                snake.extend(snake[-1:] * len(snake))
                score += 2

            # Generate a new apple
            apple, apple_color = generate_apple(snake, apple)
        else:
            # Remove tail if no apple eaten
            snake.pop()

        # Draw everything
        screen.fill(BLACK)
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
