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
    def __init__(self, move, parent, meanValue, c, sims):
        Node.__init__(self, parent)
        self.move = move #tuple: (super_space (int), sub_space (int))
        self.meanValue = meanValue
        self.c = c
        self.sims = sims
    
    def getMove(self):
        return self.move
    
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

        
#Expansion: create child node of possible move. iterate over all possible nodes parent is current state, children are next states

def validMoves(currNode, gameState):
    '''
    currNode is a moveNode object
    gameState is a ultimate_board object

    returns list of valid move tuples
    '''
    prevMove = currNode.getMove()
    moveSet = findMoves(prevMove) #this is all possible moves given blank board

    #vet possible moves
    validMoves = []
    for i in moveSet:
        if gameState.isValidMove(i):
            validMoves.append(i)
    
    return validMoves

#Simulation: find the max UCB child. continue by making random choices until end state. win = 1, draw = 0, lose = -1
#            go back to the parent, update the number of times the parent has been traversed

#Backpropagation: tally up the total score of all of the paths in the random sim. average to find v_i in Selection
#                 if the child node explores has a lot of wins, it contributes linearly to UCB (exploitation)


if __name__ == "__main__":
    testMoveHis = [('X', (1, 4)), ('O', (4, 7)), ('X', (7, 2)), ('O', (2, 7)), ('X', (7, 9)), ('O', (9, 7)), ('X', (7, 3)), ('O', (3, 7)), ('X', (7, 8)), ('O', (8, 5)), ('X', (5, 4)), ('O', (4, 4)), ('X', (4, 5)), ('O', (5, 1)), ('X', (1, 2)), ('O', (2, 3)), ('X', (3, 4)), ('O', (4, 6)), ('X', (6, 5))]
    testUltBoard = ult.ultimate_board()
    for i in testMoveHis:
        chip = i[0]
        super_space = i[1][0]
        sub_space = i[1][1]
        testUltBoard.placeChip(chip, super_space, sub_space)
    

    prevMove = testMoveHis[-1][1]
    print(testUltBoard)
    print("test 1: out of bounds super_space")
    move = (10, 1)
    print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")
    
    print("test 2: out of bounds sub_space")
    move = (2, 11)
    print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    print("test 3: out of bounds super_space and sub_space")
    move = (12, 13)
    print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    print("test 4: invalid super_space") 
    move = (1, 3)
    print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    print("test 5: invalid sub_space")
    move = (5, 1)
    print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    print("test 6: valid move")
    move = (5, 6)
    print("expected:", True, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")