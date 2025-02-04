import pygame
import sys
import random
import heapq

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

# Directions: Right, Left, Down, Up
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_valid(x, y, snake_body, grid_size):
    """Check if a position is within the grid and not part of the snake."""
    return 0 <= x < grid_size and 0 <= y < grid_size and (x, y) not in snake_body


def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(snake_head, food, snake_body, grid_size):
    """Find a path from the snake's head to the food using A*."""
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(snake_head, food), 0, snake_head, []))  # f, g, position, path
    came_from = {}
    g_score = {snake_head: 0}
    closed_list = set()

    while open_list:
        _, current_g, current, path = heapq.heappop(open_list)

        if current == food:
            return path + [current]

        closed_list.add(current)

        # Explore all possible directions
        for dx, dy in DIRECTIONS:
            next_x, next_y = current[0] + dx, current[1] + dy
            next_pos = (next_x, next_y)

            if next_pos not in closed_list and is_valid(next_x, next_y, snake_body, grid_size):
                new_g = current_g + 1
                if next_pos not in g_score or new_g < g_score[next_pos]:
                    g_score[next_pos] = new_g
                    f_score = new_g + heuristic(next_pos, food)
                    heapq.heappush(open_list, (f_score, new_g, next_pos, path + [current]))
                    came_from[next_pos] = current

    return None  # No path found


def simulate_snake_movement(snake_body, path):
    """Simulate the snake's movement along a path."""
    simulated_snake = snake_body[:]
    for pos in path:
        simulated_snake.insert(0, pos)  # Add the next position to the head
        simulated_snake.pop()  # Remove the tail
    return simulated_snake


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
    global screen
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Snake Game with A*")

    clock = pygame.time.Clock()

    # Initialize snake and food
    snake = [(0, 0)]  # Snake starts at the top-left corner
    food = place_food(snake, GRID_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Use A* to find a path to the food
        path = astar(snake[0], food, snake, GRID_SIZE)

        if not path or len(path) < 2:
            print("Game Over! No valid moves.")
            running = False
            continue

        # Move the snake
        next_pos = path[1]
        snake.insert(0, next_pos)

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