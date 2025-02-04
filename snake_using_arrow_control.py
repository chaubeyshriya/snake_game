import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)  
RED = (255, 0, 0)    

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Function to draw grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))  # Vertical lines
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))  # Horizontal lines

# Function to draw snake
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Function to move the snake
def move_snake(snake_body, direction):
    head_x, head_y = snake_body[0]

    if direction == 'UP':
        head_y -= CELL_SIZE
    elif direction == 'DOWN':
        head_y += CELL_SIZE
    elif direction == 'LEFT':
        head_x -= CELL_SIZE
    elif direction == 'RIGHT':
        head_x += CELL_SIZE

    new_head = (head_x, head_y)
    snake_body.insert(0, new_head)
    snake_body.pop()


def check_fruit_collision(snake_head, fruit_pos):
    return snake_head == fruit_pos

# Function to spawn a new fruit
def spawn_fruit():
    return (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

# Main game loop
def main():
    clock = pygame.time.Clock()

    # Initial snake position and direction
    snake_body = [(100, 100), (80, 100), (60, 100)]
    direction = 'RIGHT'

    # Spawn the first fruit
    fruit_pos = spawn_fruit()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key presses for snake direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Move the snake
        move_snake(snake_body, direction)

        # Check if the snake eats the fruit
        if check_fruit_collision(snake_body[0], fruit_pos):
            snake_body.append(snake_body[-1])  
            fruit_pos = spawn_fruit()  

        # Check for snake collision with itself or the walls
        head_x, head_y = snake_body[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()  # Game over if the snake hits the wall
        for segment in snake_body[1:]:
            if segment == (head_x, head_y):
                pygame.quit()
                sys.exit()  # Game over if the snake collides with itself

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the grid
        draw_grid()

        # Draw the snake
        draw_snake(snake_body)

        # Draw the fruit
        pygame.draw.rect(screen, RED, pygame.Rect(fruit_pos[0], fruit_pos[1], CELL_SIZE, CELL_SIZE))

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(10)  # Lower FPS for more control

if __name__ == "__main__":
    main()