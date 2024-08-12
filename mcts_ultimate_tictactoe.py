#Monte Carlo Tree Search for Ult TicTacToe

import ultimate_tictactoe as ult
import random
import numpy as np

class Node(object):
    def __init__(self, parent):
        '''
        parent is Node object
        '''
        self.parent = parent
        self.children = []
    
    def addChildren(self, childNode):
        self.children.append(childNode)

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children
    

#Selection: finds state value of all possible next moves, pick the one 
#           with highest value
# UCB(s_i) = v_i + C*sqrt(log(N)/n_i)
# v_i: mean value of node
# C: constant to balance exploitation/exploration 
# N: # of sims done on parent node (consistent state increases score)
# n_i: # of sims done on current child node (unexplored increases score)

# first does random, since you don't know anything about the state values yet

class moveNode(Node):
    def __init__(self, parent, meanValue, c, sims):
        Node.__init__(self, parent)
        self.meanValue = meanValue
        self.c = c
        self.sims = sims
    
    def getMeanValue(self):
        return self.meanValue
    
    def getC(self):
        return self.c
    
    def getSims(self):
        return self.sims
    
    def UCB(self, childNode):
        '''
        childNode is moveNode object
        '''
        if childNode.getSims() == 0:
            return 2**32 - 1
        
        else:
            result = childNode.getMeanValue() + childNode.getC() * np.sqrt(np.log(childNode.getParentSims())/childNode.getCurrSims())
            return result
    
    def findMaxUCB(self):
        ucb_list = []
        #self.children can be mapped one to one with ucb_list via list indices
        for i in range(len(self.children)):
            ucb_list.append(self.UCB(self.children[i]))
        
        max_ucb = max(ucb_list)
        max_ucb_index = ucb_list.index(max_ucb)

        return self.children[max_ucb_index]
    

def findTotMoves():
    
    tot_move_set = []
    for i in range(1, 10):
        for j in range(1, 10):
            tot_move_set.append((i, j))

    return tot_move_set

def findMoves(prev_move):
    '''
    prev_move = (prev_super, prev_sub) (tuple)
    prev_super: int representing previous super space played
    prev_sub: int representing previous sub space played
    '''
    possible_moves = []
    for i in range(1, 10):
        possible_moves.append((prev_move[1], i))
    
    return possible_moves

        
#Expansion: look at next moves. parent is current state, children are next states

def expansion(currNode):

#Simulation: find the max UCB child. continue by making random choices until end state. win = 1, draw = 0, lose = -1
#            go back to the parent, update the number of times the parent has been traversed

#Backpropagation: tally up the total score of all of the paths in the random sim. average to find v_i in Selection
#                 if the child node explores has a lot of wins, it contributes linearly to UCB (exploitation)









if __name__ == "__main__":
    test = moveNode(1, 2, 3, 4)
    test.meanValue
    

