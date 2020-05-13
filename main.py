import pygame
import math
from grid import Grid

'''
Project TODO:
    - Add event handling to inside the algorithms running

'''

def main():
    WIN_SIZE = (800, 600)

    # Dimensions for Cells
    # WIDTH, HEIGHT, MARGIN
    CELL_DIM = (20, 20, 5)

    grid = Grid(WIN_SIZE, CELL_DIM)

    # initalize pygame window
    pygame.init()
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Pathfinding Visualizer")

    # clock object to limit speed
    clock = pygame.time.Clock()

    isRunning = True

    mouseDragging = False

    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDragging = True
                pos = pygame.mouse.get_pos()
                col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])
                grid.setWall(row, col)
            elif event.type == pygame.MOUSEMOTION:
                if mouseDragging:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                    row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])
                    grid.setWall(row, col)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDragging = False
            elif event.type == pygame.KEYDOWN:
                # Pressing the r key resets the entire grid
                if event.key == pygame.K_c:
                    grid.clear()
                elif event.key == pygame.K_r:
                    grid.reset()
                # Pressing the s key sets the source square
                elif event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                    row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])
                    grid.toggleSource(row, col)        
                # Pressing the t key sets the target square
                elif event.key == pygame.K_t:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                    row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])
                    grid.toggleTarget(row, col)
                elif event.key == pygame.K_1:
                    grid.BFS(screen, clock)
                elif event.key == pygame.K_2:
                    grid.DFS(screen, clock)
                elif event.key == pygame.K_3:
                    grid.aStarSearch(screen, clock)
        # end for

        draw(grid, screen)

        clock.tick(60)
    # end while

    pygame.quit()

def draw(grid, screen):
    screen.fill((105, 105, 105))
    grid.drawGrid(screen)
    pygame.display.flip()


if __name__ == '__main__':
    main()