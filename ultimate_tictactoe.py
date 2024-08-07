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

    def boardChip(self, player):
        board_state = self.checkGameWon(player) #(bool, player)
        
        if board_state[0]:
            return player.getChip()

    def placeChip(self, player, loc):
        '''
        input
        loc: int 1-9 to represent board location
        player: player class, whoever's turn it is

        return
        None, mutates board
        '''
        chip = player.getChip() #stores the chip that's to be placed
        
        if loc not in [1,2,3,4,5,6,7,8,9]:
            raise ValueError("not a valid board space")
        else:

            row_index_selected = (loc - 1) // 3
            row_space_selected = loc % 3 - 1

            if self.rowlst[row_index_selected][row_space_selected] in self.valid_chips:
                raise AssertionError("space taken: assumes space is vacant")
            
            self.rowlst[row_index_selected][row_space_selected] = chip


    
    def __str__(self):        
        result = self.rowstr(self.row1) + "\n" + self.rowstr(self.row2) + "\n" + self.rowstr(self.row3)
        return result

class ultimate_board(board):
    def __init__(self, valid_chips = ['X', 'O']):
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
    
    def placeChip(self, player, loc, subloc):
        '''
        input
        player: player class
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

        sub_board_selected.placeChip(player, subloc)

        
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
    
    def __str__(self):

        return self.display_board()
    

def play():
    
    player1 = player('player 1', '')
    player2 = player('player 2', '')

    
    if player1.getChip() == player2.getChip():
        raise ValueError('players must choose different chips')

    ultboard = ultimate_board()
    
    prevChosen = False # indicates whether there is a restriction to which board you can play in

    while (not player1.getWinState()) or (not player2.getWinState()):
        #player 1 turn
        print("---------------------------------")
        print(f"player 1 turn ({player1.getChip()})")
        print("---------------------------------")
        validSuperSpace1 = False
        
        if not prevChosen:
            while not validSuperSpace1:
                try:
                    player1superchoice = int(input('choose super board space: '))
                    subboard = ultboard.selectSubBoard(player1superchoice)
                    assert subboard.checkGameWon(player1)[0] == False
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
                subboard.placeChip(player1, player1subchoice)
                validSuperSpace1 = True
            except ValueError:
                print('invalid board space selected, try again')
            except AssertionError:
                print('must select space that has not already been selected, try again')
            else:
                break     
        
        nextSuperBoard = player1subchoice

        print(ultboard)
        if ultboard.checkGameWon(player1):
            player1.updateWinState()
            print(player1.getWinState())
            print('player 1 won, exiting loop')
            break

        #player 2 turn
        print("---------------------------------")
        print(f"player 2 turn ({player2.getChip()})")
        print("---------------------------------")
        
        print("current superboard: ", nextSuperBoard)
        subboard = ultboard.selectSubBoard(nextSuperBoard)
        print(subboard)

        validSubSpace2 = False

        while not validSubSpace2:
            try:
                prompt_str = 'choose sub board space: '
                player2subchoice = int(input(prompt_str))
                subboard.placeChip(player2, player2subchoice)
                validSuperSpace1 = True
            except ValueError:
                print('invalid board space selected, try again')
            except AssertionError:
                print('must select space that has not already been selected, try again')
            else:
                break
        
        nextSuperBoard = player2subchoice
        
        print(ultboard)
        if ultboard.checkGameWon(player2):
            player2.updateWinState()
            print(player2.getWinState())
            print('player 2 won, exiting loop')
            break

if __name__ == "__main__":
    play()