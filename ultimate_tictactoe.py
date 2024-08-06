class player(object):
    def __init__(self, name, chip = '', win_state = False, valid_chips = ['X', 'O']):
        '''
        chip: player's chip in valid_chips
        win_state: whether the player has won (default False)
        valid_chips: list of possible chips (default ['X', 'O'])
        '''
        
        while chip not in valid_chips:
            print("chip must be a valid chip")
            print("valid chips: ", valid_chips)
            chip = input('What chip would you like (X or O)')
        
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
                raise ValueError("space taken")
            
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
        print(result)

        return result

    def display_board(self):
        result = []
        board_lst = self.init_board_lst() # len = 3, each entry len = 9
        combined_board_lst = []
        for i in board_lst:
            combined_board_lst.extend(i)
        final_result = [[], [], [], [], [], [], [], [], []]
        # current problem: it's basically taking board_list and turning rows to columns,
        # whereas it needs to kind of put them into clusters of three instead       
        
        # for i in range(len(board_lst[0])):
        #     for k in range(len(board_lst)):
        #         final_result[i%9].append(board_lst[k][i])
        
        # for i in range(len(combined_board_lst)): # len = 27
        #     final_result_indx = i // 3
        #     final_result[final_result_indx].append(combined_board_lst[i])
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
    
class gameplay(object):
    def __init__(self):
        
        player1 = player('player 1', '')
        player2 = player('palyer 2', '')
        if player1.getChip() == player2.getChip():
            raise ValueError('players must choose different chips')
        self.player1 = player1
        self.player2 = player2

        ultboard = ultimate_board()
        self.ultboard = ultboard

    pass

if __name__ == "__main__":
    # player1 = player()
    # player1.updateWinState()
    # print(player1.getWinState())
    player1 = player('X')

    # board1 = board()
    # board1.placeChip(player1, 1)
    # board1.placeChip(player1, 5)
    # board1.placeChip(player1, 9)
    # print(board1)
    # print(board1.checkGameWon(player1))

    ult = ultimate_board()
    ult.placeChip(player1, 1, 1)
    ult.placeChip(player1, 1, 2)
    ult.placeChip(player1, 1, 3)
    ult.placeChip(player1, 5, 1)
    ult.placeChip(player1, 5, 5)
    ult.placeChip(player1, 5, 9)
    ult.placeChip(player1, 9, 2)
    ult.placeChip(player1, 9, 5)
    ult.placeChip(player1, 9, 8)
    print(ult)
    print(ult.getWonBoards(player1))
    print(ult.row1[0].boardChip(player1))
    print(ult.checkGameWon(player1))
    # this is a test line!
    # this is another test line i made