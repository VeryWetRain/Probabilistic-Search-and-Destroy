import numpy as np
import random as rand
import itertools
from graphics import *

## DISPLAY MAP
DISPLAY_MAP = 0
## DISPLAY BELIEF GRID
DISPLAY_BELIEF = 0
## SIZE OF ENVIRONMENT
DIMENSIONS = 50
## SIZE OF BOXES IN ENVIRONMENT
BOX_SIZE = 10
## TARGET TEXT SIZE (5-32)
TARGET_TEXT_SIZE = 10
## BELIEF TEXT SIZE (5-32)
BELIEF_TEXT_SIZE = 10
## AGENT TYPE (1-3)
AGENT_TYPE = 1
## MOVING TARGET (0-1)
MOVING_TARGET = 0
## SEARCH COUNT
SEARCH_COUNT = 0
## TARGET LOCATION
TARGET_X = 0
TARGET_Y = 0
## MINIMUM PROBABILITY (ADVANCED AGENT)
MIN_PROB = 0.01
## MAX SEARCHES
MAX_SEARCHES = 10
## CURRENT CELL
CUR_CELL = ()

## GENERATE NUMPY GRID FOR ENVIRONMENT AND BELIEF
map = np.zeros((DIMENSIONS,DIMENSIONS))
belief_map = np.zeros((DIMENSIONS,DIMENSIONS))

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
        TARGET_X = rand.randint(0, DIMENSIONS-1)
        TARGET_Y = rand.randint(0, DIMENSIONS-1)

        environment_box(TARGET_X, TARGET_Y, "X")

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
def update_box():
    ## CALC PROBABILITY REDUCTION
    prob_reduc = belief_map[TARGET_X][TARGET_Y] * (1 - map[TARGET_X][TARGET_Y])

    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            ## ON CELL SEARCHED (DONT UPDATE LIKE THE OTHERS)
            if(TARGET_X==i & TARGET_Y==j):
                belief_map[TARGET_X][TARGET_Y] = belief_map[TARGET_X][TARGET_Y] - prob_reduc
            ## INCREASE PROBABILITY BASED ON REDUCED PROBABILITY FROM TARGET CELL
            else:
                belief_map[TARGET_X][TARGET_Y] = belief_map[TARGET_X][TARGET_Y] + belief_map[TARGET_X][TARGET_Y] * prob_reduc



## CHECK IF TARGET IS IN CELL
def query_cell(x,y):
    ## TARGET IN CELL
    if(TARGET_X == x & TARGET_Y == y):
        ## TARGET IS IN CELL BUT NOT FOUND DUE TO TERRAIN
        if(map[x][y] <= rand.uniform(0,1)):
            return False
        ## TARGET IS FOUND
        else:
            return True
    ## TARGET NOT IN CELL
    else:
        return False


def falseNeg(x, y):
    cell = map[x][y]
    if cell == 0:
        return 0.1
    elif cell == 1:
        return 0.3
    elif cell == 2:
        return 0.7
    elif cell == 3:
        return 0.9


def manhattenDistance(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def distanceMatrix(x1, y1):
    mat = np.zeros((DIMENSIONS, DIMENSIONS))
    for x2 in range(DIMENSIONS):
        for y2 in range(DIMENSIONS):
            mat[x2][y2] = manhattenDistance(x1, y1, x2, y2)
    return mat


def moveRule1(x, y):
    # use distance matrix to account for distance
    distMatrix = distanceMatrix(x, y)
    logMatrix = 1 + np.log(1 + distMatrix)
    rule1matrix = belief / logMatrix

    maxValx, maxValy = np.unravel_index(np.argmax(rule1matrix, axis=None), belief.rule1matrix)
    maxVals = []
    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            if belief[i][j] == belief[maxValx][maxValy]:
                maxVals.append((i, j))
    randnum = rand.randint(1, len(maxVals)) - 1
    return maxVals[randnum]


def moveRule2():
    return NotImplementedError


# logic for playing game, turn by turn
def play(rule):
    iter = 0
    if rule == 1:
        while True:
            x, y = moveRule1()
            if query_cell(x, y):
                print("Target found, YAY!")
                break;
            else:
                updateBelief(x, y)
            iter += 1
    elif rule == 2:
        while True:
            x, y = moveRule2()
            if query_cell(x, y):
                print("Target found, YAY!")
                break;
            else:
                updateBelief(x, y)
            iter += 1




## MAIN
if __name__ == "__main__":
    try:
        #update_box(win, 5, 5, "1")

        ## CREATE ENVIRONMENT
        searchanddestroy = Environment()

        ## RANDOM CELL TO START
        CUR_CELL_X = rand.randint(0, DIMENSIONS-1)
        CUR_CELL_Y = rand.randint(0, DIMENSIONS-1)

        ## SEARCH FOR TARGET
        while(MAX_SEARCHES <= SEARCH_COUNT):
            ## IF TARGET FOUND
            if(query_cell(CUR_CELL_X,CUR_CELL_Y)):
                print("Target Found, Search Count = ", SEARCH_COUNT)
                break
            ## PROCEED BASED ON AGENT TYPE
            else:
                update_box()

                if(AGENT_TYPE == 1):
                    print("argmax = ", belief_map.argmax())

                #elif(AGENT_TYPE == 2):

                #elif(AGENT_TYPE == 3):

            SEARCH_COUNT+=1



        print(belief[1][1])
        ## PAUSE AFTER CLOSING
        win.getMouse()
    except KeyboardInterrupt:
        print("Game Over!")


    #jamesbond = Agent(searchanddestroy)
    #jamesbond.play()

    # If no axis mentioned, then it works on the entire array
    #print(np.argmax(array))