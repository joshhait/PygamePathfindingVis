import pygame
import math
import util
import time

'''
VALUES OF GRID:
    0 - Empty square
    1 - Wall
    2 - Source
    3 - Target
    4 - Discovered
    5 - Explored
    6 - Path
'''

class Grid:
    def __init__(self, WIN_SIZE, CELL_DIM):
        self.rows = math.floor(WIN_SIZE[1]/(CELL_DIM[1]+CELL_DIM[2]))
        self.cols = math.floor(WIN_SIZE[0]/(CELL_DIM[0]+CELL_DIM[2]))

        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

        self.source = (None, None)
        self.target = (None, None)

        self.cellWidth = CELL_DIM[0]
        self.cellHeight = CELL_DIM[1]
        self.cellMargin = CELL_DIM[2]

    def getGrid(self):
        return self.grid

    def getElement(self, row, col):
        return self.grid[row][col]

    def setElement(self, row, col, val):
        self.grid[row][col] = val

    def setWall(self, row, col):
        """
            Sets a wall at grid[row][col]. Can't set a wall on top of the source/target square.
        """
        if self.grid[row][col] != 2 and self.grid[row][col] != 3:
            self.grid[row][col] = 1
            #print("Wall set at (", row, ", ", col, ")")
    
    def removeWall(self, row, col):
        self.grid[row][col] = 0

    def getRows(self):
        return self.rows

    def getCols(self):
        return self.cols

    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = 0
        self.source = (None, None)
        self.target = (None, None)
    
    def getSource(self):
        return self.source

    def setSource(self, row, col):
        self.source = (row, col)
        self.grid[row][col] = 2

    def removeSource(self):
        row = self.source[0]
        col = self.source[1]
        self.grid[row][col] = 0
        self.source = (None, None)

    def getTarget(self):
        return self.target

    def setTarget(self, row, col):
        self.target = (row, col)
        self.grid[row][col] = 3

    def removeTarget(self):
        row = self.target[0]
        col = self.target[1]
        self.grid[row][col] = 0
        self.target = (None, None)

    def isTarget(self, node):
        return (node == self.target)

    def drawGrid(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                color = (255, 255, 255)
                if self.grid[row][col] == 1:
                    color = (0, 0, 0)
                elif self.grid[row][col] == 2:
                    color = (0, 255, 0)
                elif self.grid[row][col] == 3:
                    color = (255, 0, 0)
                elif self.grid[row][col] == 4:
                    color = (0, 206, 209)
                elif self.grid[row][col] == 5:
                    color = (0, 0, 128)
                elif self.grid[row][col] == 6:
                    color = (255, 255, 0)
                pygame.draw.rect(   screen, 
                                    color, 
                                    [(self.cellMargin + self.cellWidth) * col + self.cellMargin, 
                                    (self.cellMargin + self.cellHeight) * row + self.cellMargin, 
                                    self.cellWidth, 
                                    self.cellHeight])

    def getSuccessors(self, node):
        row, col = node[0], node[1]
        successors = []
        if row - 1 >= 0 and self.grid[row-1][col] != 1:
            pos = (row-1, col)
            north = (pos, 'North', 1)
            successors.append(north)
        if col + 1 < self.cols and self.grid[row][col+1] != 1:
            pos = (row, col+1)
            east = (pos, 'East', 1)
            successors.append(east)
        if row + 1 < self.rows and self.grid[row+1][col] != 1:
            pos = (row+1, col)
            south = (pos, 'South', 1)
            successors.append(south)
        if col - 1 >= 0 and self.grid[row][col-1] != 1:
            pos = (row, col-1)
            west = (pos, 'West', 1)
            successors.append(west)
        return successors

    def BFS(self, screen, clock):
        """
            Uses BFS to find path from source node to target node.
            TODO: add visuals (i.e. change values  of grid so that draw shows it "visualizing")
        """
        if self.source == (None, None) or self.target == (None, None):
            print("Source or Target is not set! Aborting BFS...")
            return False

        targetFound = False

        explored, path = [], []

        startPos = self.getSource()

        fringe = util.Queue()

        fringe.push((startPos, path))

        while not fringe.isEmpty():
            pygame.event.pump()

            currNode, currPath = fringe.pop()

            if currNode in explored:
                continue

            explored.append(currNode)

            if self.isTarget(currNode):
                targetFound = True
                break

            for succ in self.getSuccessors(currNode):
                nextXY = succ[0]
                nextDir = succ[1]
                nextCost = succ[2]
                if nextXY != self.getSource() and nextXY != self.getTarget() and self.grid[nextXY[0]][nextXY[1]] == 0:
                    self.grid[nextXY[0]][nextXY[1]] = 4
                    screen.fill((105, 105, 105))
                    self.drawGrid(screen)
                    pygame.display.flip()
                    clock.tick(60)

                pathToSucc = currPath + [nextXY]

                fringe.push((nextXY, pathToSucc))

            if currNode != self.getSource() and currNode != self.getTarget():
                self.grid[currNode[0]][currNode[1]] = 5
                screen.fill((105, 105, 105))
                self.drawGrid(screen)
                pygame.display.flip()
                clock.tick(60)

        if targetFound:
            for node in currPath:
                if node != self.getTarget():
                    self.grid[node[0]][node[1]] = 6

    def DFS(self, screen, clock):
            """
                Uses DFS to find path from source node to target node.
                TODO: add visuals (i.e. change values  of grid so that draw shows it "visualizing")
            """
            if self.source == (None, None) or self.target == (None, None):
                print("Source or Target is not set! Aborting DFS...")
                return False

            targetFound = False

            explored, path = [], []

            startPos = self.getSource()

            fringe = util.Stack()

            fringe.push((startPos, path))

            while not fringe.isEmpty():
                pygame.event.pump()
                currNode, currPath = fringe.pop()

                if currNode in explored:
                    continue

                explored.append(currNode)

                if self.isTarget(currNode):
                    targetFound = True
                    break

                for succ in self.getSuccessors(currNode):
                    nextXY = succ[0]
                    nextDir = succ[1]
                    nextCost = succ[2]
                    if nextXY != self.getSource() and nextXY != self.getTarget() and self.grid[nextXY[0]][nextXY[1]] == 0:
                        self.grid[nextXY[0]][nextXY[1]] = 4
                        screen.fill((105, 105, 105))
                        self.drawGrid(screen)
                        pygame.display.flip()
                        clock.tick(60)

                    pathToSucc = currPath + [nextXY]

                    fringe.push((nextXY, pathToSucc))

                if currNode != self.getSource() and currNode != self.getTarget():
                    self.grid[currNode[0]][currNode[1]] = 5
                    screen.fill((105, 105, 105))
                    self.drawGrid(screen)
                    pygame.display.flip()
                    clock.tick(60)

            if targetFound:
                for node in currPath:
                    if node != self.getTarget():
                        self.grid[node[0]][node[1]] = 6

    def aStarSearch(self, screen, clock):
        if self.source == (None, None) or self.target == (None, None):
            print("Source or Target is not set! Aborting BFS...")
            return False

        targetFound = False

        explored, path = [], []

        startPos = self.getSource()

        fringe = util.PriorityQueue()

        fringe.push((startPos, path), self.manhattanHeuristic(startPos))

        while not fringe.isEmpty():
            pygame.event.pump()
            currNode, currPath = fringe.pop()

            if currNode in explored:
                continue

            explored.append(currNode)

            if self.isTarget(currNode):
                targetFound = True
                break

            for succ in self.getSuccessors(currNode):
                nextXY = succ[0]
                nextDir = succ[1]
                nextCost = succ[2]
                if nextXY != self.getSource() and nextXY != self.getTarget() and self.grid[nextXY[0]][nextXY[1]] == 0:
                    self.grid[nextXY[0]][nextXY[1]] = 4
                    screen.fill((105, 105, 105))
                    self.drawGrid(screen)
                    pygame.display.flip()
                    clock.tick(60)

                pathToSucc = currPath + [nextXY]

                gn = self.getCostOfActions(pathToSucc)
                hn = self.manhattanHeuristic(nextXY)
                fn = gn + hn 

                fringe.push((nextXY, pathToSucc), fn)

            if currNode != self.getSource() and currNode != self.getTarget():
                self.grid[currNode[0]][currNode[1]] = 5
                screen.fill((105, 105, 105))
                self.drawGrid(screen)
                pygame.display.flip()
                clock.tick(60)

        if targetFound:
            for node in currPath:
                if node != self.getTarget():
                    self.grid[node[0]][node[1]] = 6

    def manhattanHeuristic(self, pos):
        xy1 = pos
        xy2 = self.getTarget()
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def getCostOfActions(self, actions):
        cost = 0
        for action in actions:
            cost += 1
        return cost