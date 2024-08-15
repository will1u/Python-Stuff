import tkinter as tk
from tkinter import messagebox

class player(object):
    def __init__(self, name, chip = '', win_state = False, valid_chips = ['X', 'O']):
        '''
        chip: player's chip in valid_chips
        win_state: whether the player has won (default False)
        valid_chips: list of possible chips (default ['X', 'O'])
        '''
        
        while chip not in valid_chips:
            print("---------------------------------")
            print("chip must be a valid chip")
            print("valid chips: ", valid_chips)
            chip = input(f'{name} choose chip (X or O)')
            print("---------------------------------")
        
        self.name = name
        self.chip = chip
        self.win_state = win_state
        self.valid_chips = valid_chips

    def updateWinState(self):
        self.win_state = True

    def getWinState(self):
        return self.win_state

    def getChip(self):
        return self.chip
    
    def __str__(self):
        return self.name
    
class board(object):
    def __init__(self, valid_chips = ['X', 'O'], win_state = False,):

        

        self.valid_chips = valid_chips
        self.win_state = win_state
        self.row1 = ["1","2","3"]
        self.row2 = ["4","5","6"]
        self.row3 = ["7","8","9"]
        self.rowlst = [self.row1, self.row2, self.row3]


        # player1 = player.__init__(self, valid_chips)
        # player2 = player.__init__(self, valid_chips)
    def rowstr(self, row):
        """
        outputs a string for that represents 
        a given row on the board
        """
        rowstr = ", ".join(row)
        rowstr = "[" + rowstr + "]"
        return rowstr

    def getRowLst(self):
        return self.rowlst

    def checkGameWon(self, player):
        """
        checks whether there is a win 
        player: player class

        returns tuple (bool, player) representing winstate of given player
        """
        mark = player.getChip()
        game_won = False
        if self.row1[0] == self.row1[1] == self.row1[2] == mark:
            game_won = True
        elif self.row2[0] == self.row2[1] == self.row2[2] == mark:
            game_won = True
        elif self.row3[0] == self.row2[1] == self.row2[2] == mark:
            game_won = True
        elif self.row1[0] == self.row2[1] == self.row3[2] == mark:
            game_won = True
        elif self.row1[2] == self.row2[1] == self.row3[0] == mark:
            game_won = True
        elif self.row1[0] == self.row2[0] == self.row3[0] == mark:
            game_won = True
        elif self.row1[1] == self.row2[1] == self.row3[1] == mark:
            game_won = True
        elif self.row1[2] == self.row2[2] == self.row3[2] == mark:
            game_won = True
        
        if game_won:
            player.updateWinState()
        
        return (game_won, player)
    
    def checkGameWonGeneral(self):
        '''
        True if board is won
        False if not
        does not depend on passing a player   
        '''
        game_won = False
        if self.row1[0] == self.row1[1] == self.row1[2]:
            game_won = True
        elif self.row2[0] == self.row2[1] == self.row2[2]:
            game_won = True
        elif self.row3[0] == self.row2[1] == self.row2[2]:
            game_won = True
        elif self.row1[0] == self.row2[1] == self.row3[2]:
            game_won = True
        elif self.row1[2] == self.row2[1] == self.row3[0]:
            game_won = True
        elif self.row1[0] == self.row2[0] == self.row3[0]:
            game_won = True
        elif self.row1[1] == self.row2[1] == self.row3[1]:
            game_won = True
        elif self.row1[2] == self.row2[2] == self.row3[2]:
            game_won = True
        
        return game_won
    
    def isFilled(self):
        for i in self.rowlst:
            for j in i:
                if j in self.valid_chips:
                    continue
                else:
                    return False
        return True        
        
    def isDraw(self):
        if self.checkGameWonGeneral():
            return False
        else:
            if self.isFilled():
                return True
            else:
                return False

    def boardChip(self, player):
        board_state = self.checkGameWon(player) #(bool, player)
        
        if board_state[0]:
            return player.getChip()

    def placeChip(self, player_chip, loc):
        '''
        input
        loc: int 1-9 to represent board location
        player: player class, whoever's turn it is

        return
        None, mutates board
        '''
        
        if loc not in [1,2,3,4,5,6,7,8,9]:
            raise ValueError("not a valid board space")
        else:

            row_index_selected = (loc - 1) // 3
            row_space_selected = loc % 3 - 1

            if self.rowlst[row_index_selected][row_space_selected] in self.valid_chips:
                raise AssertionError("space taken: assumes space is vacant")
            
            self.rowlst[row_index_selected][row_space_selected] = player_chip

    def isValidMove(self, loc):
        '''
        loc is int in 1-9 inclusive
        '''
        if loc not in range(1, 10):
            return False
        elif self.checkGameWonGeneral() or self.isDraw():
            return False
        else:
            row_index_selected = (loc - 1) // 3
            row_space_selected = loc % 3 - 1
            if self.rowlst[row_index_selected][row_space_selected] in self.valid_chips:
                return False
            
            else:
                return True

    
    def __str__(self):        
        result = self.rowstr(self.row1) + "\n" + self.rowstr(self.row2) + "\n" + self.rowstr(self.row3)
        return result

class ultimate_board(board):
    def __init__(self, valid_chips = ['X', 'O']):
        
        self.player1 = player('player 1', '')
        self.player2 = player('player 2', '')

        self.board1 = board()
        self.board2 = board()
        self.board3 = board()
        self.board4 = board()
        self.board5 = board()
        self.board6 = board()
        self.board7 = board()
        self.board8 = board()
        self.board9 = board()

        self.row1 = [self.board1, self.board2, self.board3]
        self.row2 = [self.board4, self.board5, self.board6]
        self.row3 = [self.board7, self.board8, self.board9]
        self.rowlst = [self.row1, self.row2, self.row3]
        self.valid_chips = valid_chips


    def ultRowStr(self, ult_row):
        """
        ult_row is a 9x3 list (9 entries, each len 3)
        """
        result = []
        for i in ult_row:
            result.append(" | ".join(i))
        
        return result
    
    def selectSubBoard(self, loc):
        if loc not in [1,2,3,4,5,6,7,8,9]:
            raise ValueError("not a valid board space")

        super_row_index_selected = (loc - 1) // 3
        super_row_space_selected = loc % 3 - 1
        sub_board_selected = self.rowlst[super_row_index_selected][super_row_space_selected] # this is a board object

        return sub_board_selected
    
    def placeChip(self, player_chip, loc, subloc):
        '''
        input
        player_chip: player's chip string
        loc: super board loc
        subloc: sub board loc

        return
        None, mutates the board
        '''
        if loc not in [1,2,3,4,5,6,7,8,9]:
            raise ValueError("not a valid board space")
        
        if subloc not in [1,2,3,4,5,6,7,8,9]:
            raise ValueError("not a valid board space")
        
        super_row_index_selected = (loc - 1) // 3
        super_row_space_selected = loc % 3 - 1
        sub_board_selected = self.rowlst[super_row_index_selected][super_row_space_selected] # this is a board object

        sub_board_selected.placeChip(player_chip, subloc)

        
    def init_board_lst(self):
        result = [[],[],[]]
        for result_indx in range(len(result)):

            for j in self.rowlst[result_indx]:

                for i in range(3):
                    result[result_indx].append(self.rowstr(j.getRowLst()[i]))

        return result

    def display_board(self):
        result = []
        board_lst = self.init_board_lst() # len = 3, each entry len = 9
        combined_board_lst = []
        for i in board_lst:
            combined_board_lst.extend(i)
        final_result = [[], [], [], [], [], [], [], [], []]

        row = 0
        for i in range(len(board_lst)): #len = 3
            final_result[3*row].extend(board_lst[i][0::3])
            final_result[3*row + 1].extend(board_lst[i][1::3])
            final_result[3*row + 2].extend(board_lst[i][2::3])
            
            row += 1

        result = self.ultRowStr(final_result)
        result.insert(3,"_"*len(result[2]))
        result.insert(7,"_"*len(result[2]))
        
        result_str = "\n".join(result)
        return result_str
    
    def getWonBoards(self, player):
        '''
        input: player
        return: tuple (wonBoards (list), player)
        '''
        wonBoards = []
        for i in self.rowlst:
            for j in i: # access each of the subboards
                boardState = j.checkGameWon(player) # tuple: (bool, player)
                if boardState[0]:
                    wonBoards.append(j)
        
        return (wonBoards, player)
    
    def checkGameWon(self, player):
        '''
        checks if the ultimate board 
        has been won by player

        returns True if won, False if not
        '''
        wonBoardsList = self.getWonBoards(player)[0]
        wonBoardsSet = set(wonBoardsList)

        winConditions = []
        for i in self.rowlst: 
            winConditions.append(set(i)) #rows
        for i in range(3): 
            winConditions.append({self.rowlst[0][i], self.rowlst[1][i], self.rowlst[2][i]}) #columns
        winConditions.append({self.rowlst[0][0], self.rowlst[1][1], self.rowlst[2][2]}) #diag 1
        winConditions.append({self.rowlst[0][2], self.rowlst[1][1], self.rowlst[2][0]}) #diag 2

        return wonBoardsSet in winConditions
    
    def isValidMove(self, move, prevMove):
        '''
        move is a tuple (super_space (int), sub_space (int))
        prevMove is a tuple (super_space (int), sub_space (int))
        assumes prevMove is a valid move

        prevMove = None expresses that move is the first move in the game
        '''
        #super_space checks
        if (move[0] not in range(1,10)) or (move[1] not in range(1, 10)):
            return False
        elif prevMove == None:
            return True
        elif move[0] != prevMove[1]:
            sub_board = self.selectSubBoard(prevMove[1])
            if not(sub_board.checkGameWonGeneral() or sub_board.isDraw()):
                return False
            else:
                '''
                implement checking the move
                '''
                sub_board = self.selectSubBoard(move[0])
                return sub_board.isValidMove(move[1])
        elif move == prevMove:
            return False
        
        #sub_space checks
        sub_board = self.selectSubBoard(move[0])
        
        if not(sub_board.checkGameWonGeneral() or sub_board.isDraw()):
            if sub_board in self.getFilledBoardsGeneral(): 
                return False
            else:
                return sub_board.isValidMove(move[1])



    def getFilledBoardsGeneral(self):
        '''
        returns list of boards that are won by either player or drawn
        '''
        filledBoards = []
        for i in self.rowlst:
            for j in i:
                if j.checkGameWonGeneral() or j.isDraw():
                    filledBoards.append(j)

        return filledBoards

    def isDraw(self):
        '''
        returns True for draw, False for not
        '''
        filledBoardsGeneral = self.getFilledBoardsGeneral()
        if len(filledBoardsGeneral) == 9:
            if self.checkGameWon(self.player1) or self.checkGameWon(self.player2):
                return False
            else:
                return True
        else:
            return False
    
    def __str__(self):

        return self.display_board()
    

def play():
    '''
    returns moveLog: list of moves made 
    entries in list: (move, player_chip)
    move is a tuple (super_space, sub_space)
    player is a player object
    '''
    
    ultboard = ultimate_board()
    moveLog = []

    if ultboard.player1.getChip() == ultboard.player2.getChip():
        raise ValueError('players must choose different chips')

    
    
    prevChosen = False # indicates whether there is a restriction to which board you can play in

    while (not ultboard.player1.getWinState()) or (not ultboard.player2.getWinState()):
        #player 1 turn
        print("---------------------------------")
        print(f"player 1 turn ({ultboard.player1.getChip()})")
        print("---------------------------------")
        validSuperSpace1 = False
        
        if not prevChosen:
            while not validSuperSpace1:
                try:
                    player1superchoice = int(input('choose super board space: '))
                    subboard = ultboard.selectSubBoard(player1superchoice)
                    assert subboard.checkGameWon(ultboard.player1)[0] == False
                    validSuperSpace1 = True
                except ValueError:
                    print('invalid board space selected, try again')
                except AssertionError:
                    print('must select board that has not been won, try again')
                else:
                    break
            prevChosen = True
        
        else:
            print("current superboard: ", nextSuperBoard)
            subboard = ultboard.selectSubBoard(nextSuperBoard)
            print(subboard)

        validSubSpace1 = False

        while not validSubSpace1:
            try:
                prompt_str =  'choose sub board space: '
                player1subchoice = int(input(prompt_str))
                subboard.placeChip(ultboard.player1.getChip(), player1subchoice)
                validSuperSpace1 = True
            except ValueError:
                print('invalid board space selected, try again')
            except AssertionError:
                print('must select space that has not already been selected, try again')
            else:
                break     
        
        if moveLog == []: #accounts for fact that only on the first turn does someone get free choice
                           #of super space
            player1move = (player1superchoice, player1subchoice)
            player1log = (ultboard.player1.getChip(), player1move)
            moveLog.append(player1log)
        
        else:
            player1move = (nextSuperBoard, player1subchoice)
            player1log = (ultboard.player1.getChip(), player1move, )
            moveLog.append(player1log)
        

        nextSuperBoard = player1subchoice

        print(ultboard)
        if ultboard.checkGameWon(ultboard.player1):
            ultboard.player1.updateWinState()
            print(ultboard.player1.getWinState())
            print('player 1 won, exiting loop')
            return moveLog
            break
        
        stopOption = input('stop game? (yes/else)')
        if stopOption == 'yes':
            return moveLog
        #player 2 turn
        print("---------------------------------")
        print(f"player 2 turn ({ultboard.player2.getChip()})")
        print("---------------------------------")
        
        print("current superboard: ", nextSuperBoard)
        subboard = ultboard.selectSubBoard(nextSuperBoard)
        print(subboard)

        validSubSpace2 = False

        while not validSubSpace2:
            try:
                prompt_str = 'choose sub board space: '
                player2subchoice = int(input(prompt_str))
                subboard.placeChip(ultboard.player2.getChip(), player2subchoice)
                validSuperSpace1 = True
            except ValueError:
                print('invalid board space selected, try again')
            except AssertionError:
                print('must select space that has not already been selected, try again')
            else:
                break
        
        player2move = (nextSuperBoard, player2subchoice)
        player2log = (ultboard.player2.getChip(), player2move)
        moveLog.append(player2log)
        
        nextSuperBoard = player2subchoice
        
        print(ultboard)
        if ultboard.checkGameWon(ultboard.player2):
            ultboard.player2.updateWinState()
            print(ultboard.player2.getWinState())
            print('player 2 won, exiting loop')
            return moveLog
            


if __name__ == "__main__":
    moveLog = play()
    print(moveLog)