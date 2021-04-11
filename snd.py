import numpy as np
import random as rand
import itertools
from graphics import *

## SUPPRESS OUTPUT
QUIET = 1
## DISPLAY MAP
DISPLAY_MAP = 0
## DISPLAY BELIEF GRID
DISPLAY_BELIEF = 0
## SIZE OF ENVIRONMENT
DIMENSIONS = 50
## SIZE OF BOXES IN ENVIRONMENT
BOX_SIZE = 20
## TARGET TEXT SIZE (5-32)
TARGET_TEXT_SIZE = 20
## BELIEF TEXT SIZE (5-32)
BELIEF_TEXT_SIZE = 10
## AGENT TYPE (1-3)
AGENT_TYPE = 3
## MOVING TARGET (0-1)
MOVING_TARGET = 0
## SEARCH COUNT
SEARCH_COUNT = 0
## TARGET LOCATION
TARGET_X = rand.randint(0, DIMENSIONS - 1)
TARGET_Y = rand.randint(0, DIMENSIONS - 1)
## MINIMUM PROBABILITY (ADVANCED AGENT)
MIN_PROB = 0.01
## MAX SEARCHES
MAX_SEARCHES = 100000000
## CURRENT CELL
CUR_CELL = ()
## SET NUMPY PRECISION
np.set_printoptions(precision=3)

## GENERATE NUMPY GRID FOR ENVIRONMENT AND BELIEF
map = np.zeros((DIMENSIONS,DIMENSIONS))

## GENERATE NUMPY GRID FOR BELIEF
belief = np.full((DIMENSIONS,DIMENSIONS), 1/(DIMENSIONS*DIMENSIONS))

## GENERATE MAP FOR DISPLAY IN WINDOW
if DISPLAY_MAP:
    win = GraphWin(width=DIMENSIONS * BOX_SIZE, height=DIMENSIONS * BOX_SIZE)
## SET THE COORDINATES FOR THE WINDOW
#win.setCoords(0, DIMENSIONS * BOX_SIZE, DIMENSIONS * BOX_SIZE, 0)

def setupEnvironment():
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


## DRAW ENVIRONMENT
def environment_box(x, y, txt):
    if DISPLAY_MAP:
        ## SHOW TARGET LOCATION
        if txt == "X":
            label = Text(Point(y * BOX_SIZE + BOX_SIZE / 2, x * BOX_SIZE + BOX_SIZE / 2), txt)
            label.setFill("red")
            label.setSize(TARGET_TEXT_SIZE)
            label.draw(win)
        ## COLOR GRID
        else:
            mySquare = Rectangle(Point(y * BOX_SIZE, x * BOX_SIZE), Point(y * BOX_SIZE + BOX_SIZE, x * BOX_SIZE + BOX_SIZE))
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
def updateBelief():
    ## CALC COMMON DENOMINATOR USING MARGINALIZATION PRIOR TO CHANGING CURRENT CELL BELIEF
    denominator = ((1 - belief[CUR_CELL_X][CUR_CELL_Y]) + map[CUR_CELL_X][CUR_CELL_Y] * belief[CUR_CELL_X][CUR_CELL_Y])
    #print("denominator : ", denominator)

    ## UPDATE BELIEF FOR CURRENT CELL
    belief[CUR_CELL_X][CUR_CELL_Y] = belief[CUR_CELL_X][CUR_CELL_Y] * map[CUR_CELL_X][CUR_CELL_Y] / denominator
    #print("reducing ", CUR_CELL_X, " ", CUR_CELL_Y, " to ", belief[CUR_CELL_X][CUR_CELL_Y])

    ## UPDATE BELIEF FOR ALL OTHER CELLS
    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            if(CUR_CELL_X!=i or CUR_CELL_Y!=j):
                belief[i][j] = belief[i][j] / denominator
                #print("increasing ", i,j," to ", belief[i][j])

## CHECK IF TARGET IS IN CELL
def query_cell(x,y):
    ## TARGET IN CELL
    if(TARGET_X == x and TARGET_Y == y):
        ## TARGET IS IN CELL BUT NOT FOUND DUE TO TERRAIN
        if(map[x][y] <= rand.uniform(0,1)):
            return False
        ## TARGET IS FOUND
        else:
            return True
    ## TARGET NOT IN CELL
    else:
        return False

## CHECK IF NORMALIZATION NEEDS TO BE PERFORMED (NOT NEEDED)
def normalization_check():
    total_probability = 0

    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            total_probability += belief[i][j]

    #print("total probability : ", total_probability)
    #print("total probability numpy : ", belief.sum())


## FIND NEXT BEST CELL TO SEARCH
def next_search():
    ## ACCESS SOME GLOBALS
    global SEARCH_COUNT
    global CUR_CELL_X
    global CUR_CELL_Y

    ## SET MAX AND MIN VARIABLES
    max_prob = -1
    distance = DIMENSIONS*DIMENSIONS
    nearest_x = -1
    nearest_y = -1

    #print("Max Prob = ", max_prob)

    if (AGENT_TYPE == 1):
        ## GET MAX PROBABILITY FROM BELIEF MAP
        max_prob = belief.max()
        if QUIET == 0: print("Max Prob = ", max_prob)

        ## FIND NEAREST CELL WITH MAX PROB
        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                if(belief[i][j] == max_prob):
                    dtmp = abs(i-CUR_CELL_X)+abs(j-CUR_CELL_Y)
                    if(dtmp <= distance):
                        if QUIET == 0: print("map[", i, "][" ,j, "] distance : ",dtmp)
                        nearest_x = i
                        nearest_y = j
                        distance = dtmp

    elif (AGENT_TYPE == 2):
        ## GET MAX PROBABILITY FROM BELIEF MAP
        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                if (belief[i][j] * (1-map[i][j]) > max_prob): max_prob = belief[i][j] * (1-map[i][j])
        if QUIET == 0: print("Max Prob = ", max_prob)

        ## FIND NEAREST CELL WITH MAX PROB
        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                if QUIET == 0: print("map[", i, "][", j, "] probability : ", belief[i][j]*(1-map[i][j]))
                if(belief[i][j]*(1-map[i][j]) == max_prob):
                    dtmp = abs(i-CUR_CELL_X)+abs(j-CUR_CELL_Y)
                    if(dtmp <= distance):
                        if QUIET == 0: print("map[", i, "][" ,j, "] distance : ",dtmp)
                        nearest_x = i
                        nearest_y = j
                        distance = dtmp
    elif (AGENT_TYPE == 3):
        ## ONLY CHANGE TARGET IF MINIMUM PROBABILITY THRESHOLD IS MET
        if(belief[CUR_CELL_X][CUR_CELL_Y] * (1-map[CUR_CELL_X][CUR_CELL_Y]) < MIN_PROB):
            ## GET MAX PROBABILITY FROM BELIEF MAP
            for i in range(DIMENSIONS):
                for j in range(DIMENSIONS):
                    if (belief[i][j] * (1-map[i][j]) > max_prob): max_prob = belief[i][j] * (1-map[i][j])
            if QUIET == 0: print("Max Prob = ", max_prob)

            ## FIND NEAREST CELL WITH MAX PROB
            for i in range(DIMENSIONS):
                for j in range(DIMENSIONS):
                    if QUIET == 0: print("map[", i, "][", j, "] probability : ", belief[i][j]*(1-map[i][j]))
                    if(belief[i][j]*(1-map[i][j]) == max_prob):
                        dtmp = abs(i-CUR_CELL_X)+abs(j-CUR_CELL_Y)
                        if(dtmp <= distance):
                            if QUIET == 0: print("map[", i, "][" ,j, "] distance : ",dtmp)
                            nearest_x = i
                            nearest_y = j
                            distance = dtmp

    if QUIET == 0: print("nearest_x:nearest_y:distance - ", nearest_x," : ", nearest_y, " : ", distance)
    SEARCH_COUNT+= distance
    CUR_CELL_X = nearest_x
    CUR_CELL_Y = nearest_y


def move_target():
    ## ACCESS SOME GLOBALS
    global TARGET_X
    global TARGET_Y

    prob = rand.uniform(0, 1)

    ## CANT MOVE UP
    if(TARGET_X == 0):
        ## CANT MOVE UP AND LEFT
        if (TARGET_Y == 0):
            if (prob <= .5): TARGET_X += 1
            else: TARGET_Y += 1
        ## CANT MOVE UP AND RIGHT
        elif (TARGET_Y == DIMENSIONS - 1):
            if (prob <= .5): TARGET_X += 1
            else: TARGET_Y -= 1
        else:
            if (prob <= .33): TARGET_X += 1
            elif (prob > .33 and prob <= .66): TARGET_Y += 1
            else: TARGET_Y -= 1
    ## CANT MOVE DOWN
    elif (TARGET_X == DIMENSIONS-1):
        ## CANT MOVE DOWN AND LEFT
        if (TARGET_Y == 0):
            if (prob <= .5): TARGET_X -= 1
            else: TARGET_Y += 1
        ## CANT MOVE DOWN AND RIGHT
        elif (TARGET_Y == DIMENSIONS - 1):
            if (prob <= .5): TARGET_X -= 1
            else: TARGET_Y -= 1
        else:
            if (prob <= .33): TARGET_X -= 1
            elif (prob > .33 and prob <= .66): TARGET_Y += 1
            else: TARGET_Y -= 1
    ## CANT MOVE LEFT
    elif (TARGET_Y == 0):
        if (prob <= .33): TARGET_Y += 1
        elif (prob > .33 and prob <= .66): TARGET_X += 1
        else: TARGET_X -= 1
    ## CANT MOVE RIGHT
    elif (TARGET_Y == DIMENSIONS-1):
        if (prob <= .33): TARGET_Y -= 1
        elif (prob > .33 and prob <= .66): TARGET_X += 1
        else: TARGET_X -= 1
    ## MOVEMENT NOT RESTRICTED
    else:
        if(prob <= .25): TARGET_X += 1
        elif (prob > .25 and prob <= .5): TARGET_X -= 1
        elif (prob > .5 and prob <= .75): TARGET_Y += 1
        elif (prob > .75): TARGET_Y -= 1



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


def generateRule2Matrix():
    mat = belief.copy()

    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            mat[i][j] *= (1 - falseNeg(i, j))
    return mat


def move(x, y, rule):
    # use distance matrix to account for distance
    distMatrix = distanceMatrix(x, y)
    logMatrix = 1 + np.log(1 + distMatrix)
    if rule == 1:
        matrix = belief / logMatrix
    else:
        matrix = generateRule2Matrix() / logMatrix

    maxValx, maxValy = np.unravel_index(np.argmax(matrix, axis=None), belief.matrix)
    maxVals = []
    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            if belief[i][j] == belief[maxValx][maxValy]:
                maxVals.append((i, j))
    randnum = rand.randint(1, len(maxVals)) - 1
    return maxVals[randnum]

# logic for playing game, turn by turn
def play(rule):
    iter = 0
    if rule == 1:
        while True:
            x, y = move()
            if query_cell(x, y):
                print("Target found, YAY!")
                break;
            else:
                updateBelief(x, y)
            iter += 1
    elif rule == 2:
        while True:
            x, y = move()
            if query_cell(x, y):
                print("Target found, YAY!")
                break;
            else:
                updateBelief(x, y)
            iter += 1






## MAIN
if __name__ == "__main__":
    try:
        ## CREATE ENVIRONMENT
        setupEnvironment()
        ## SHOW TARGET IN ENVIRONMENT
        environment_box(TARGET_X, TARGET_Y, "X")
        print("TARGET AT : ", TARGET_X, ",", TARGET_Y)
        print("TARGET in : ", map[TARGET_X][TARGET_Y])

        ## RANDOM CELL TO START
        CUR_CELL_X = rand.randint(0, DIMENSIONS-1)
        CUR_CELL_Y = rand.randint(0, DIMENSIONS-1)

        ## SEARCH FOR TARGET
        while(MAX_SEARCHES >= SEARCH_COUNT):
            SEARCH_COUNT += 1

            ## SEARCH INITIAL CELL
            if QUIET == 0:print("searching cell : ",CUR_CELL_X,",",CUR_CELL_Y)
            if QUIET == 0:print("belief")
            if QUIET == 0:print(belief)

            ## IF TARGET FOUND
            if(query_cell(CUR_CELL_X,CUR_CELL_Y)):
                print("Target Found, Search Count = ", SEARCH_COUNT)
                break
            ## PROCEED BASED ON AGENT TYPE
            else:
                if MOVING_TARGET == 1: move_target()
                #print("Target Not Found")
                updateBelief()
                #normalization_check()
                next_search()
                ## UPDATE TARGET POSITION ON DISPLAY
                if MOVING_TARGET == 1: environment_box(TARGET_X, TARGET_Y, "X")
                print("TARGET AT : ", TARGET_X, ",", TARGET_Y)
                print("TARGET in : ", map[TARGET_X][TARGET_Y])

        ## PAUSE AFTER CLOSING
        if DISPLAY_MAP: win.getMouse()
    except KeyboardInterrupt:
        print("Done")


