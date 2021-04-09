import numpy as np
import random as rand
import itertools
from graphics import *

## DISPLAY MAP
DISPLAY_MAP = 0
## DISPLAY BELIEF GRID
DISPLAY_BELIEF = 0
## SIZE OF ENVIRONMENT
DIMENSIONS = 10
## SIZE OF BOXES IN ENVIRONMENT
BOX_SIZE = 40
## TARGET TEXT SIZE (5-32)
TARGET_TEXT_SIZE = 24
## BELIEF TEXT SIZE (5-32)
BELIEF_TEXT_SIZE = 10
## AGENT TYPE (1-3)
AGENT_TYPE = 1
## MOVING TARGET (0-1)
MOVING_TARGET = 0
## SEARCH COUNT
SEARCH_COUNT = 0
## TARGET LOCATION
target_x = 0
target_y = 0

## GENERATE NUMPY GRID FOR ENVIRONMENT
map = np.zeros((DIMENSIONS,DIMENSIONS))

## GENERATE NUMPY GRID FOR BELIEF
belief = np.full((DIMENSIONS,DIMENSIONS), 1/(DIMENSIONS*DIMENSIONS))

## GENERATE MAP FOR DISPLAY IN WINDOW
win = GraphWin(width=DIMENSIONS * BOX_SIZE, height=DIMENSIONS * BOX_SIZE)
## SET THE COORDINATES FOR THE WINDOW
win.setCoords(0, DIMENSIONS * BOX_SIZE, DIMENSIONS * BOX_SIZE, 0)


class Environment():
    def __init__(self):

        # each cell randomly generated as flat, hilly, forest, cave with 0.25 chance each
        # legend for map:
        # 0: flat
        # 1: hilly
        # 2: forest
        # 3: cave
        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                prob = rand.uniform(0,1)
                if prob <= 0.25:
                    map[i][j] = .1
                    environment_box(i, j, "0")
                elif prob > 0.25 and prob <= 0.5:
                    map[i][j] = .3
                    environment_box(i, j, "1")
                elif prob > 0.5 and prob <= 0.75:
                    map[i][j] = .7
                    environment_box(i, j, "2")
                else:
                    map[i][j] = .9
                    environment_box(i, j, "3")

        # randomly choose a cell as the target, doesn't matter where as long as uniformly random
        target_x = rand.randint(0, DIMENSIONS-1)
        target_y = rand.randint(0, DIMENSIONS-1)

        environment_box(target_x, target_y, "X")

## DRAW ENVIRONMENT
def environment_box(x, y, txt):

    ## SHOW TARGET LOCATION
    if txt == "X":
        label = Text(Point(x * BOX_SIZE + BOX_SIZE / 2, y * BOX_SIZE + BOX_SIZE / 2), txt)
        label.setFill("red")
        label.setSize(TARGET_TEXT_SIZE)
        label.draw(win)
    ## COLOR GRID
    else:
        mySquare = Rectangle(Point(x * BOX_SIZE, y * BOX_SIZE), Point(x * BOX_SIZE + BOX_SIZE, y * BOX_SIZE + BOX_SIZE))
        if (txt == "0"):
            mySquare.setFill("white")
        elif (txt == "1"):
            mySquare.setFill("tan")
        elif (txt == "2"):
            mySquare.setFill("green")
        elif (txt == "3"):
            mySquare.setFill("grey")
        mySquare.draw(win)

## UPDATE BELIEF BOX VALUES
def update_box(x, y, txt):

    ## SHOW TARGET LOCATION
    if txt == "X":
        label = Text(Point(x * BOX_SIZE + BOX_SIZE / 2, y * BOX_SIZE + BOX_SIZE / 2), txt)
        label.setFill("red")
        label.draw(win)
    ## COLOR GRID
    else:
        mySquare = Rectangle(Point(x * BOX_SIZE, y * BOX_SIZE), Point(x * BOX_SIZE + BOX_SIZE, y * BOX_SIZE + BOX_SIZE))
        if (txt == "0"):
            mySquare.setFill("white")
        elif (txt == "1"):
            mySquare.setFill("tan")
        elif (txt == "2"):
            mySquare.setFill("green")
        elif (txt == "3"):
            mySquare.setFill("grey")
        mySquare.draw(win)

## CHECK IF TARGET IS IN CELL
def query_cell(x,y):
    ## TARGET IN CELL
    if(target_x == x & target_y == y):
        ## TARGET IS IN CELL BUT NOT FOUND DUE TO TERRAIN
        if(map[x][y] <= rand.uniform(0,1)):
            return False
        ## TARGET IS FOUND
        else:
            return True
    ## TARGET NOT IN CELL
    else:
        return False

class Agent:
    def __init__(self, environment):

        # agent's belief state
        self.belief_state = np.full((DIMENSIONS,DIMENSIONS), 1/(DIMENSIONS*DIMENSIONS))
        self.mat = environment


    def falseNeg(self, x, y):
        cell = self.mat[x][y]
        if cell == 0:
            return 0.1
        elif cell == 1:
            return 0.3
        elif cell == 2:
            return 0.7
        elif cell == 3:
            return 0.9


    def updateBelief(self, row, col):
        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                if row != i or col != j:
                    belief[i][j] = belief[i][j] + belief[row][col]*(1-self.falseNeg(i, j)) * (belief[i][j]/(1-belief[row][col]))
        belief[row][col] = belief[row][col] * self.falseNeg(row, col)


    def manhattenDistance(self, x1, x2, y1, y2):

    def moveRule1(self):

    def moveRule2(self):

    # logic for playing game, turn by turn
    def play(self, rule):
        iter = 0
        if rule == 1:
            while True:
                x, y = self.moveRule1()
                if query_cell(x, y):
                    print("Target found, YAY!")
                    break;
                else:
                    self.updateBelief(x, y)
                iter += 1
        elif rule == 2:
            while True:
                x, y = self.moveRule2()
                if query_cell(x, y):
                    print("Target found, YAY!")
                    break;
                else:
                    self.updateBelief(x, y)
                iter += 1




## MAIN
if __name__ == "__main__":
    try:
        #update_box(win, 5, 5, "1")

        ## CREATE ENVIRONMENT
        searchanddestroy = Environment()

        ## PAUSE AFTER CLOSING
        win.getMouse()
    except KeyboardInterrupt:
        print("Game Over!")


    #jamesbond = Agent(searchanddestroy)
    #jamesbond.play()

    # If no axis mentioned, then it works on the entire array
    #print(np.argmax(array))