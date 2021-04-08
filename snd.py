import numpy as np
import random as rand
import itertools

class Environment:
    def __init__(self):
        # generate 50x50 grid
        self.map = np.zeros((50,50))

        # each cell randomly generated as flat, hilly, forest, cave with 0.25 chance each
        # legend for map:
        # 0: flat
        # 1: hilly
        # 2: forest
        # 3: cave
        for i in range(50):
            for j in range(50):
                prob = rand.uniform(0,1)
                if prob <= 0.25:
                    self.map[i][j] = 0
                elif prob > 0.25 and prob <= 0.5:
                    self.map[i][j] = 1
                elif prob > 0.5 and prob <= 0.75:
                    self.map[i][j] = 2
                else:
                    self.map[i][j] = 3

        # randomly choose a cell as the target, doesn't matter where as long as uniformly random
        x = rand.randint(0, 50)
        y = rand.randint(0, 50)
        self.target = (x, y)

class Agent:
    def __init__(self, environment):

        # agent's belief state
        self.belief_state = np.full((50,50), 1/2500)

    # logic for playing game, turn by turn
    def play(self):

    def updateBelief(self):

    def manhattendistance(self, x1, x2, y1, y2):

        
if __name__ == "__main__":
    searchanddestroy = Environment()
    jamesbond = Agent(searchanddestroy)
    jamesbond.play()