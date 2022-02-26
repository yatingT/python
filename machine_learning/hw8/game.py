import random
import copy
import numpy as np


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        
    def succ(self, state, drop_phase):
        successor=[]
        if drop_phase==True:
            for row in range(5):
                for col in range(5):
                    if state[row][col] ==' ':
                        temp_state=copy.deepcopy(state)
                        temp_state[row][col]=self.my_piece
                        successor.append(temp_state)
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        
                        for i in range(row-1,row+1):
                            for j in range(col-1,col+1):             
                                try:
                                    if state[i][j] ==' ':
                                        temp_state=copy.deepcopy(state)
                                        temp_state[row][col] =' '
                                        temp_state[i][j] =self.my_piece
                                        successor.append(temp_state)
                                except IndexError:
                                    continue
        return successor


    def make_move(self, state):
        drop_phase = True  # set drop_phase to True
        move=[]
        if state==[[' ' for j in range(5)] for i in range(5)]:
            print(True)
            (row, col) = (random.randint(0,4), random.randint(0,4))
            move.insert(0, (row,col))  
            return move
        
        b = sum((i.count('b') for i in state))
        r = sum((i.count('r') for i in state))
        if b >= 4 and r >= 4:
            drop_phase = False

        if not drop_phase:
            value, after = self.max_value(state, 0,drop_phase)
            diff = np.array(state) == np.array(after)
            comp = np.where(diff == False) 
            if state[comp[0][0]][comp[1][0]] == ' ':
                (row,col) = (comp[0][0], comp[1][0])
                (oldr, oldc) = (comp[0][1],comp[1][1])
            else:
                (row, col) = (comp[0][1], comp[1][1])
                (oldr, oldc) = (comp[0][0], comp[1][0])
            move.insert(0, (row, col))
            move.insert(1, (oldr, oldc)) 
            return move
        
        value, after = self.max_value(state,0,drop_phase)
        diff = np.array(state) == np.array(after)
        comp = np.where(diff == False) 
        (row,col) = (comp[0][0], comp[1][0])
        if state[row][col] != ' ': 
            (row, col) = (comp[0][0], comp[1][0])
        move.insert(0, (row,col))  
        return move
            
            
    def opponent_move(self, move):
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        print(move)
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(5):
                if col==2:
                    continue
                elif col==0 or col ==1:
                    if state[row][col] != ' 'and state[row][col]==state[row+1][col+1]==state[row+2][col+2]==state[row+3][col+3]:
                        return 1 if state[row][col]==self.my_piece else -1
                elif col == 3 or col ==4:
                    if state[row][col] != ' 'and state[row][col]==state[row-1][col-1]==state[row-2][col-2]==state[row-3][col-3]:
                        return 1 if state[row][col]==self.my_piece else -1
                    
        # TODO: check 3x3 square corners wins
        for row in range(1,3):
            for col in range(1,3):
                if state[row][col]==' ' and state[row-1][col-1]==state[row-1][col+1]==state[row+1][col-1]==state[row+1][col+1] != ' ':
                    return 1 if state[row][col]==self.my_piece else -1

        return 0 # no winner yet
    
    def heuristic_game_value(self, state):
        result=self.game_value(state)
        if result==1 or result== -1:
            return result
        weight=0.25
        value=0
        #horizontal
        me=[self.my_piece,' ']
        oppo=[self.opp,' ']
        for row in range(5):
            for col in range(5):
                if state[row][col]!=' ':
                    temp=0
                    # check horiznontal 
                    if col<2:
                        temp=0
                        for i in range(4):
                            if state[row][col+i] not in me:
                                break
                            else:
                                if state[row][col+i] == self.my_piece:
                                    temp+=weight
                    if temp>value:
                        value = temp
                    
                    #check vertical 
                    if row<2:
                        temp=0
                        for i in range(4):
                            if state[row+i][col] not in me:
                                break
                            else:
                                if state[row+i][col] == self.my_piece:
                                    temp+=weight
                    if temp>value:
                        value = temp
                        
                    #check right diagnal 
                    if row<2 and col<2:
                        temp =0
                        for i in range(4):
                            if state[row+i][col+i] not in me:
                                break
                            else:
                                if state[row+i][col+i] == self.my_piece:
                                    temp+=weight
                    if temp>value:
                        value = temp
                        
                    #check left diagnal 
                    if col>2 and row <2:
                        temp =0
                        for i in range(4):
                            if state[row+i][col-i] not in me:
                                break
                            else:
                                if state[row+i][col-i] == self.my_piece:
                                    temp+=weight
                    if temp>value:
                        value = temp
                    
                    #check corner
                    if row in range (1,3) and col in range(1,3):
                        temp =0
                        for row in range(1,3):
                            for col in range(1,3):
                                if state[row][col]==' ':
                                    if state[row-1][col-1] not in me or state[row-1][col+1] not in me or state[row+1][col-1] not in me or state[row+1][col+1] not in me:
                                            break
                                    else:
                                        if state[row-1][col-1] ==self.my_piece:
                                            temp+=weight
                                        if state[row-1][col+1] ==self.my_piece:
                                            temp+=weight
                                        if state[row+1][col-1] ==self.my_piece:
                                            temp+=weight
                                        if state[row+1][col+1] ==self.my_piece:
                                            temp+=weight
                    if temp>value:
                        value = temp      
        return value
    
    def max_value(self, state, depth,drop_phase):
        after = state
        result=self.game_value(state)
        if result != 0:
            return result,after
        if depth>=2:
            return self.heuristic_game_value(state),after
        else:
            alpha = float('-Inf')
            next_step=self.succ(state, drop_phase)
            for s in next_step :
                next_min = self.min_value(s,depth+1,drop_phase)
                if next_min[0] > alpha:
                    alpha = next_min[0]
                    after = s
        return alpha, after

    def min_value(self, state, depth,drop_phase):
        after = state
        result=self.game_value(state)
        if result !=0:
            return result,after
        if depth>=2:
            return self.heuristic_game_value(state),after

        else:
            beta = float('Inf')
            next_step=self.succ(state, drop_phase)
            for s in next_step:
                next_max = self.max_value(s,depth+1,drop_phase)
                if next_max[0] < beta:
                    beta = next_max[0]
                    after = s
        return beta, after



############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            print(move)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()