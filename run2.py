from __future__ import division
from copy import deepcopy
from mcts2 import mcts

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

bestBoard=None
bestScore=0
it=0
values=[]
class BeansOrCorn():
    def __init__(self,n):
        self.board = [[1 for col in range(n)] for row in range(n)]

    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    possibleActions.append(Action(plant=2, x=i, y=j))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.plant
        return newState

    def isTerminal(self):
        count=0
        n=len(self.board)
        for row in self.board:
            for el in row:
                if(el==2):
                    count+=1
        if(count>(n/2)*(n+1)/2):
            return True
        else:
            return False

    def getReward(self):
        n=len(self.board)
        sum=0
        ar=self.board
        for x in range(n):
            for y in range(n):
                corn = 0
                bean = 0
                if(x!=0):
                    if(y!=0):
                        if(ar[x-1][y-1]==1):
                            bean+=1
                        else:
                            corn+=1
                    if(y!=n-1):
                        if(ar[x-1][y+1]==1):
                            bean+=1
                        else:
                            corn+=1
                    if(ar[x-1][y]==1):
                        bean+=1
                    else:
                        corn+=1
                if(x!=n-1):
                    if(y!=0):
                        if(ar[x+1][y-1]==1):
                            bean+=1
                        else:
                            corn+=1
                    if(y!=n-1):
                        if(ar[x+1][y+1]==1):
                            bean+=1
                        else:
                            corn+=1
                    if(ar[x+1][y]==1):
                        bean+=1
                    else:
                        corn+=1
                if(y!=0):
                    if(ar[x][y-1]==1):
                        bean+=1
                    else:
                        corn+=1
                if(y!=n-1):
                    if(ar[x][y+1]==1):
                        bean+=1
                    else:
                        corn+=1

                if(ar[x][y]==1):
                    if(corn>0):
                        sum+=15
                    else:
                        sum+=10
                else:
                    sum+=(10+bean)
        global it
        global bestBoard
        global bestScore
        global plt
        if(sum>bestScore):
            bestBoard=ar
            bestScore=sum
        if(it%100==0):
            print("Rollout: "+str(it))
            print(sum)
            values.append(sum)
        it+=1

        return sum


class Action():
    def __init__(self, plant, x, y):
        self.plant = plant
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y, self.plant))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y and self.plant == other.plant

    def __hash__(self):
        return hash((self.x, self.y, self.plant))


for i in range(12,16):
    print("Farm is "+str(i)+"x"+str(i))
    bestBoard = None
    bestScore = 0
    it = 0
    values = []
    initialState = BeansOrCorn(i)
    st = mcts(iterationLimit=200000, explorationConstant=1.0)
    action = st.search(initialState=initialState)
    print(bestScore)
    print(bestBoard)
    plt.plot(values, '.')
    plt.savefig(str(i)+"_"+str(bestScore)+'_200k_mctsCSPI.png')
    print(values)
    plt.matshow(bestBoard)
    plt.savefig(str(i)+"_"+str(bestScore)+'_200k_farmCSPI.png')
    plt.clf()