import pygame
import math
from grid import Grid


'''
Pathfinding Algorithms todo: BFS, DFS, Astar, Dijkstras

Project TODO:
    - probably need to expand the grid to be a list of lists of node objects, we'll see once we start implementing pathfinding

'''

def main():
    # Width and height of the window
    WIN_SIZE = (800, 600)

    # Dimensions for Cells
    # WIDTH, HEIGHT, MARGIN
    CELL_DIM = (20, 20, 5)

    grid = Grid(WIN_SIZE, CELL_DIM)

    # initialize pygame
    pygame.init()

    # set up the screen and screen caption
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Pathfinding Visualizer")

    # clock object to limit speed
    clock = pygame.time.Clock()

    isRunning = True

    drag = False

    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
                pos = pygame.mouse.get_pos()
                col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])
                grid.setWall(row, col)
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                    row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])
                    grid.setWall(row, col)
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
            elif event.type == pygame.KEYDOWN:
                # Pressing the r key resets the entire grid
                if event.key == pygame.K_r:
                    grid.reset()
                # Pressing the s key sets the source square
                elif event.key == pygame.K_s:

                    # get the row/col of the square where the mouse is
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                    row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])

                    # if the source is not set, set it
                    if grid.getSource() == (None, None):
                        grid.setSource(row, col)
                    # if the source is set
                    else:
                        # if the source is the current square, remove it
                        if grid.getElement(row, col) == 2:
                            grid.removeSource()
                        # if the source is not the current square, remove it, and make current square the source
                        elif grid.getElement(row, col) == 0 or grid.getElement(row, col) == 1:
                            grid.removeSource()
                            grid.setSource(row, col)
                    node = (row, col)
                    print(grid.getSuccessors(node))
                    print("rows: ", grid.getRows(), " | cols: ", grid.getCols())
                # Pressing the t key sets the target square
                elif event.key == pygame.K_t:

                    # get the row/col of the square where the mouse is
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (CELL_DIM[0] + CELL_DIM[2])
                    row = pos[1] // (CELL_DIM[1] + CELL_DIM[2])

                    # if the target is not set, set it
                    if grid.getTarget() == (None, None):
                        grid.setTarget(row, col)
                    # if the target is set
                    else:
                        # if the target is the current square, remove it
                        if grid.getElement(row, col) == 3:
                            grid.removeTarget()
                        # if the target is not the current square, remove it, and make current square the target
                        elif grid.getElement(row, col) == 0  or grid.getElement(row, col) == 1: 
                            grid.removeTarget()
                            grid.setTarget(row, col)
                elif event.key == pygame.K_1:
                    grid.BFS()
                elif event.key == pygame.K_2:
                    grid.DFS()

        # tock here and update tick to tock

        draw(grid, screen)

        clock.tick(60)

    pygame.quit()

def draw(grid, screen):
    screen.fill((105, 105, 105))
    grid.drawGrid(screen)
    pygame.display.flip()


if __name__ == '__main__':
    main()