#Monte Carlo Tree Search for Ult TicTacToe
#https://ai-boson.github.io/mcts/

import ultimate_tictactoe as ult
import random
import numpy as np
import copy

class Node(object):
    def __init__(self, parent):
        '''
        parent is Node object
        '''
        self.parent = parent
        self.children = []
    
    def addChild(self, childNode):
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
    def __init__(self, move, meanValue, c, sims, parent, gameState):
        Node.__init__(self, parent)
        self.move = move #tuple: (chip (str), (super_space (int), sub_space (int)))
        self.meanValue = meanValue
        self.c = c
        self.sims = sims

        self.gameState = gameState #ultimate_board object, after playing the parent node
        

        #these are future actions, given self node has been played
        self.untried_actions = self.validMoves() 
    
    def getMove(self):
        return self.move
    
    def getMeanValue(self):
        return self.meanValue
    
    def getC(self):
        return self.c
    
    def getSims(self):
        return self.sims
    
    def getUntriedActions(self):
        return self.untried_actions

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
    

    def findTotMoves(self):
        
        tot_move_set = []
        for i in range(1, 10):
            for j in range(1, 10):
                tot_move_set.append((i, j))

        return tot_move_set

    def findMoves(self):
        '''
        returns (super_space, sub_space)
        '''
        if self.parent == None:
            return self.findTotMoves()
        
        possible_moves = []
        currMove = self.getMove()
        currSpace = currMove[1]
        currSub = currSpace[1]
        for i in range(1, 10):

            possible_moves.append((currSub, i))
        
        return possible_moves
    
    def validMoves(self): #not right, needs to implement this rule:
        #Once a small board is won by a player or it is filled completely, no more moves may
        #be played in that board. If a player is sent to such a board, 
        #then that player may play in any other board.
        '''
        finds future valid moves, given the self node has already been played

        returns list of valid move tuples
        '''
        prevMove = self.getMove()[1]
        nextSubID = prevMove[1]
        nextSub = self.gameState.selectSubBoard(nextSubID)
        moveSet = self.findMoves() #this is all possible moves given blank board
        if self.move == None:
            return moveSet
        elif nextSub.checkGameWonGeneral() or nextSub.isDraw():
            moveSet = self.findTotMoves()
        

        #vet possible moves
        validMoves = []
        for i in moveSet:
            if self.gameState.isValidMove(i, prevMove):
                validMoves.append(i)
        
        return validMoves

    def __str__(self):
        return self.move
    
#Expansion: create child node of possible move. iterate over all possible nodes parent is current state, children are next states

    

#Simulation: find the max UCB child. continue by making random choices until end state. win = 1, draw = 0, lose = -1
#            go back to the parent, update the number of times the parent has been traversed

def simulateGame(startNode, hero, villain, gameState):
    
    '''
    performs random actions until game terminates

    startNode: the last action made before simulateGame is called
    hero: player object that refers to the player to move
    villain: the other player
    gameState: current board state before action made (ultimate_board object)

    returns 1 for win, 0 for draw, -1 for loss
    '''
    gameClone = copy.deepcopy(gameState)
    startNode.sims += 1
    currNode = startNode
    heroTurn = True #assumes startNode is villain move
    simulationPath = []
    movePath = []

    while True:
        
        if gameClone.checkGameWonGeneral():
            if gameClone.checkGameWon(hero):
                print(gameClone)
                print("sim path:")
                for i in simulationPath:
                    print(i)
                
                return 1
            else:
                print(gameClone)
                print("sim path:")
                for i in simulationPath:
                    print(i)
                return -1
        elif gameClone.isDraw():
            print(gameClone)
            print("sim path:")
            for i in simulationPath:
                print(i)
            return 0
        
        try:
            if heroTurn: #currNode is a villain move

                validMoves = currNode.getUntriedActions()
                #random future move
                if len(validMoves) == 0:
                    print(gameClone)
                random.shuffle(validMoves) #(super_space, sub_space)
                randAction = validMoves[0]
                print("valid moves: ", validMoves, " randAction: ", randAction)

                #currNode.untried_actions.remove(randAction) #untried actions is wrong: shows entire list of acitons
                
                move = (hero.getChip(), randAction)
                child = moveNode(move, 0, startNode.getC(), 0, currNode, gameClone)
                currNode.addChild(child)

                #currNode is a hero move
                currNode = child
                simulationPath.append(currNode)
                movePath.append(currNode.getMove())

                currNodeChip = currNode.getMove()[0]
                currNodeMove = currNode.getMove()[1]
                currSuper = currNodeMove[0]
                currSub = currNodeMove[1]

                print(gameClone)
                gameClone.placeChip(currNodeChip, currSuper, currSub)
                
                heroTurn = False
            
            else: #currNode is a hero move
                validMoves = currNode.getUntriedActions()
                #random future move
                if len(validMoves) == 0:
                    print(gameClone)
                random.shuffle(validMoves) #(super_space, sub_space)
                randAction = validMoves[0]
                print("valid moves: ", validMoves, " randAction: ", randAction)
                
                move = (villain.getChip(), randAction)
                child = moveNode(move, 0, startNode.getC(), 0, currNode, gameClone)
                currNode.addChild(child)
                
                #currNode is a villain move
                currNode = child
                simulationPath.append(currNode)
                movePath.append(currNode.getMove())

                currNodeChip = currNode.getMove()[0]
                currNodeMove = currNode.getMove()[1]
                currSuper = currNodeMove[0]
                currSub = currNodeMove[1]
                
                print(gameClone)
                gameClone.placeChip(currNodeChip, currSuper, currSub)

                heroTurn = True
        except:
            print("===============")
            print("code failed")
            print(movePath)
            print(gameClone)
            break

#Backpropagation: tally up the total score of all of the paths in the random sim. average to find v_i in Selection
#                 if the child node explores has a lot of wins, it contributes linearly to UCB (exploitation)


if __name__ == "__main__":
    #testMoveHis = [('X', (1, 4)), ('O', (4, 7)), ('X', (7, 2)), ('O', (2, 7)), ('X', (7, 9)), ('O', (9, 7)), ('X', (7, 3)), ('O', (3, 7)), ('X', (7, 8)), ('O', (8, 5)), ('X', (5, 4)), ('O', (4, 4)), ('X', (4, 5)), ('O', (5, 1)), ('X', (1, 2)), ('O', (2, 3)), ('X', (3, 4)), ('O', (4, 6)), ('X', (6, 5))]
    testUltBoard = ult.ultimate_board()
    # for i in testMoveHis:
    #     chip = i[0]
    #     super_space = i[1][0]
    #     sub_space = i[1][1]
    #     testUltBoard.placeChip(chip, super_space, sub_space)
    
    #villain is X hero is O

    
    move = ('X', (1, 4))
    chip = move[0]
    super_space = move[1][0]
    sub_space = move[1][1]
    
    testUltBoard.placeChip(chip, super_space, sub_space)
    currNode = moveNode(move, 1, 2, 3, None, testUltBoard)


    villain = testUltBoard.player1
    hero = testUltBoard.player2

    simulateGame(currNode, hero, villain, testUltBoard)

    #example path: simulation finds a space that has already been chosen
    # ex_path = [('O', (4, 2)), ('X', (2, 4)), ('O', (4, 6)), ('X', (6, 4)), ('O', (4, 8)), ('X', (8, 2)), ('O', (2, 7)), ('X', (7, 2)), ('O', (2, 2)), ('X', (2, 5)), ('O', (5, 7)), ('X', (7, 1)), ('O', (1, 9)), ('X', (9, 1)), ('O', (1, 5)), ('X', (5, 2)), ('O', (2, 8)), ('X', (8, 4)), ('O', (4, 4)), ('X', (4, 9)), ('O', (9, 8)), ('X', (8, 5)), ('O', (5, 4)), ('X', (4, 5)), ('O', (5, 1)), ('X', (1, 1)), ('O', (1, 7)), ('X', (7, 3)), ('O', (3, 1)), ('X', (1, 3)), ('O', (3, 9)), ('X', (9, 5))]
    # for i in ex_path:
    #     chip = i[0]
    #     super_space = i[1][0]
    #     sub_space = i[1][1]
    #     testUltBoard.placeChip(chip, super_space, sub_space)
    # print(testUltBoard)
    
    # finalNode = moveNode(ex_path[-1], 1, 2, 3, ex_path[-2], testUltBoard)
    # print(finalNode.getUntriedActions())




    # print("--------------------")
    # print("ult.isValidMoves() testing")
    # print("--------------------")
    # print("test 1: out of bounds super_space")
    # move = (10, 1)
    # print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")
    
    # print("test 2: out of bounds sub_space")
    # move = (2, 11)
    # print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    # print("test 3: out of bounds super_space and sub_space")
    # move = (12, 13)
    # print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    # print("test 4: invalid super_space") 
    # move = (1, 3)
    # print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    # print("test 5: invalid sub_space")
    # move = (5, 1)
    # print("expected:", False, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    # print("test 6: valid move")
    # move = (5, 6)
    # print("expected:", True, " actual:", testUltBoard.isValidMove(move, prevMove), "\n")

    # print("--------------------")
    # print("validMoves() testing")
    # print("--------------------")
    # print("test 1: valid moves")
    # print(currNode.validMoves(currNode, testUltBoard))
    