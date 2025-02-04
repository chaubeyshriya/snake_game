import pygame

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows  

    x = 0
    y = 0
    for l in range(rows):  # Draw vertical and horizontal lines
        x += sizeBtwn
        y += sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))  # Vertical lines
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))  # Horizontal lines

def redrawWindow(surface, width, rows):
    surface.fill((0, 0, 0))  # Black background
    drawGrid(width, rows, surface)  # Draw grid
    pygame.display.update()  # Refresh display

def main():
    width = 500  # Window width and height
    rows = 20  # Number of rows and columns
    win = pygame.display.set_mode((width, width))  # Create window
    pygame.display.set_caption("Grid Example")

    clock = pygame.time.Clock()  # Set up clock for frame rate
    flag = True

    while flag:  # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False  # Exit loop if the window is closed

        redrawWindow(win, width, rows)  # Redraw grid
        clock.tick(10)  # Limit frame rate to 10 FPS

    pygame.quit()  # Quit pygame when loop ends

if __name__ == "__main__":
    main()
