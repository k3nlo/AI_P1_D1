# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Connect 4 Module
# February 27, 2012
import copy
import random
import time

from Card import Card
from Heuristic import Heuristic
from DoubleCard.Turn import Turn
from Move import Move


class StateSpaceSearch(object):
    """ Minimax object that takes  board state
    """

    board = None

    # was using tokens x or o , work to be done we have W + R or f + e
    objectives = ['colors', 'dots']

    def __init__(self, alpha_beta, trace, board, player, turn):
        self.board = copy.deepcopy(board)
        self.row_rng = range(1, self.board.height()+1)
        self.col_rng = range(1, self.board.width()+1)
        self.player = player
        self.turn = turn
        self.en_counter = 0
        self.trace = trace
        self.alpha_beta = alpha_beta

    def createOutputFile(self, index):
        if self.alpha_beta :
            file_name = 'traceab'+str(index)+'.txt'
        else:
            file_name = 'tracemm'+str(index)+'.txt'
        text_file = open(file_name, "w")
        return text_file

    def bestMove(self, depth, board_state, curr_player_objective):
        start_time = time.time()
        print('Starting bestMove() for depth = ', depth)
        # todo: A 1 B 1 4 C 1 for recycling
        # """ Returns the best move (as a column number) and the associated alpha
        #     Calls miniMaxSearch()
        # """        # determine opponent's objective
        if curr_player_objective == self.objectives[0]:
            player_role = 'max'
        else:
            player_role = 'min'

        print('Bot role is ', player_role)

        # enumerate all legal moves
        # hashmap
        legal_moves = {}  # will map legal move states to their alpha values


        # recycling move
        # list all pickable cards
        # card history
        if self.turn.count() <= self.turn.regular_limit():
            self.bot_regular_move(depth, board_state, legal_moves, player_role)

        # todo: endless remove card loop (card history/playable cards)
        elif self.turn.count() > self.turn.regular_limit() and self.turn.count() <= self.turn.limit():

            playable_cards = []

            card_history = self.turn.card_history()
            # print('card_history = ', card_history)
            # self.turn.printHistory()
            previous_card_info = card_history[-1]
            # print('last played card: ', previous_card_info)
            previous_card_id = previous_card_info[0]

            for card in card_history:
                card_id = card[0]
                if card_id != previous_card_id:
                    card_type = int(card[1])
                    x1 = int(card[2]) #row
                    y1 = int(card[3]) #col
                    x2 = int(card[4]) #row
                    y2 = int(card[5]) #col
                    if (card_type == 1 or card_type == 3 or card_type == 5 or card_type == 7):
                        #horizontal

                        if (board_state.element(x1+1, y1) == '___' and board_state.element(x2+1, y2) == '___'):
                            # card is pickable
                            print('adding:', card)
                            playable_cards.append(card)

                    elif (card_type == 2 or card_type == 4 or card_type == 6 or card_type == 8):
                        #vertical
                        if (board_state.element(x2+1, y2) == '___'):
                            #card is pickable
                            print('adding:', card)
                            playable_cards.append(card)

            print('playable_cards', playable_cards)
            # self.bot_recycling_move_new(depth, board_state, playable_cards, legal_moves, player_role)




        if (player_role == 'max'):
            best_value = -99999999
            best_move = None
            moves = legal_moves.items()
            random.shuffle(list(moves))
            for move, value in moves:
                if value >= best_value:
                    best_value = value
                    best_move = move

        elif(player_role == 'min'):
            best_value = 99999999
            best_move = None
            moves = legal_moves.items()
            random.shuffle(list(moves))
            for move, value in moves:
                if value <= best_value:
                    best_value = value
                    best_move = move

        print('legal_moves = ', legal_moves)
        print('e(n) was run ', self.en_counter)
        elapsed_time = time.time() - start_time
        print('elapsed time: ', elapsed_time)

        if self.trace:
            file = self.createOutputFile(self.turn.count())
            file.write(str(self.en_counter))
            file.write('\n')
            file.write(str(best_value))
            file.write('\n')
            file.write('\n')
            en_values = list(legal_moves.values())
            for value in en_values:
                file.write(str(value))
                file.write('\n')
            # file.write('\n')
            file.close()

        return best_move, best_value

    def bot_regular_move(self,depth, board_state, legal_moves, player_role):
        # regular move
        # list all playable cells
        playable_cells = []
        for row in self.row_rng:
            # print('trying row', row)
            for col in self.col_rng:
                # print('trying col', col)
                if (board_state.element(row, col) == '___' and
                        board_state.element(row - 1, col) != '___'):
                    playable_cells.append(str(row) + '-' + str(col))

        # print('playable_cells: ', playable_cells)

        rotation_rng = range(1, 9)
        # in each playable cell check all the card rotation to see which one are legal

        for cell in playable_cells:
            cell_coord = cell.split('-')
            playable_row = cell_coord[0]
            playable_col = self.intToColumnLetter(int(cell_coord[1]))
            # if it is a legal regular move...
            # if self.turn.count() <= self.turn.regular_limit():
            for rotation in rotation_rng:
                move = Move('regular', rotation, playable_col, playable_row)
                if self.isLegalMove(board_state, move):
                    # make the move for curr_player
                    temp = self.makeMove(board_state, move)
                    # insert in hashmap at [key] = value
                    key = str(move.placement()) + '-' + move.dCol() + '-' + move.dRow()
                    # legal_moves[key] = self.miniMaxSearch(depth - 1, temp, player_role)
                    legal_moves[key] = self.miniMaxSearch(depth - 1, temp, player_role)

    def bot_recycling_move_new(self, depth, board_state, playable_cards, legal_moves, player_role):
        for playable_card in playable_cards:
            # pick it up the card change the state of the board run bot regular move
            x1 = int(playable_card[2])
            y1 = int(playable_card[3])
            x2 = int(playable_card[4])
            y2 = int(playable_card[5])

            # temporaly remove card
            temp_board = self.temp_remove_card(board_state, x1, y1, x2, y2)

            temp_board.printBoard()

            # # play it
            # # regular move
            # # list all playable cells
            # playable_cells = []
            # for row in self.row_rng:
            #     # print('trying row', row)
            #     for col in self.col_rng:
            #         # print('trying col', col)
            #         if (temp_board.element(row, col) == '___' and
            #                 temp_board.element(row - 1, col) != '___'):
            #             playable_cells.append(str(row) + '-' + str(col))
            #
            # # print('playable_cells: ', playable_cells)
            #
            # rotation_rng = range(1, 9)
            # # in each playable cell check all the card rotation to see which one are legal
            #
            # for cell in playable_cells:
            #     cell_coord = cell.split('-')
            #     playable_row = cell_coord[0]
            #     playable_col = self.intToColumnLetter(int(cell_coord[1]))
            #     # if it is a legal regular move...
            #     # if self.turn.count() <= self.turn.regular_limit():
            #     for rotation in rotation_rng:
            #         move = Move('regular', rotation, playable_col, playable_row)
            #         if self.isLegalMove(temp_board, move):
            #             # make the move for curr_player
            #             temp = self.makeMove(temp_board, move)
            #             # insert in hashmap at [key] = value
            #
            #             str_y1 = self.intToColumnLetter(int(y1))
            #             str_y2 =self.intToColumnLetter(int(y2))
            #             picked_card = str_y1 +'-'+str(x1)+'-'+str_y2+'-'+str(x1)
            #             key = picked_card +'-'+str(move.placement()) + '-' + move.dCol() + '-' + move.dRow()
            #             # legal_moves[key] = self.miniMaxSearch(depth - 1, temp, player_role)
            #             legal_moves[key] = self.miniMaxSearch(depth - 1, temp, player_role)
            # get score
            # in legal moves
            # put it back



    def miniMaxSearch(self, depth, board_state, role):
        # print('Starting miniMaxSearch() at depth = ', depth, 'for', role)
        # """ Searches the tree at depth 'depth'
        #     By default, the board_state is the board, and role is whomever
        #     called this miniMaxSearch
        #     Returns the alpha value
        # """
        # enumerate all legal moves from this board_state of the board
        legal_moves = []

        # regular move
        # list all playable cells
        playable_cells = []
        for row in self.row_rng:
            # print('trying row', row)
            for col in self.col_rng:
                # print('trying col', col)
                if (board_state.element(row, col) == '___' and
                        board_state.element(row - 1, col) != '___'):
                    playable_cells.append(str(row) + '-' + str(col))

        # print('playable_cells: ', playable_cells)

        rotation_rng = range(1, 9)
        # in each playable cell check all the card rotation to see which one are legal
        for cell in playable_cells:
            cell_coord = cell.split('-')
            playable_row = cell_coord[0]
            playable_col = self.intToColumnLetter(int(cell_coord [1]))
            # if it is a legal regular move...
            if self.turn.count() <= self.turn.regular_limit():
                for rotation in rotation_rng:
                    move = Move('regular', rotation, playable_col, playable_row)
                    if self.isLegalMove(board_state, move):
                        # make the move in column for curr_player
                        temp = self.makeMove(board_state, move)
                        legal_moves.append(temp)


        # if this node (board_state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(board_state):
            # return the heuristic value of node
            if(role == 'max'):
                objective = 'colors'
            else:
                objective = 'dots'
            return self.value(board_state, objective)

        # determine opponent's color todo: replace color by tokens (twice)
            # determine opponent's color /token objective
        if role == 'max':
            opponent_role = 'min'
            value = -99999999
            for child in legal_moves:
                if child == None:
                    print("child == None (miniMaxSearch)")
                value = max(value, self.miniMaxSearch(depth - 1, child, opponent_role))
            return value
        elif role == 'min':
            opponent_role = 'max'
            value = 99999999
            for child in legal_moves:
                if child == None:
                    print("child == None (miniMaxSearch)")
                value = min(value, self.miniMaxSearch(depth - 1, child, opponent_role))
            return value


    def isLegalMove(self, board_state, move):
        """ Boolean function to check if making the move (inserting a card at (x1, y1)(x2, y2)) is a legal move
        """
        move_is_legal = False
        # regular move
        if (move.type() == 'regular'):
            card = Card()
            coord = self.turn.initialize_move(card, move)
            is_valid = self.turn.bot_validate_regular(board_state, card, self.row_rng, self.col_rng, coord[0], coord[1], coord[2], coord[3])
            if is_valid:
                move_is_legal = True

        # recycling move
        if (move.type()=='recycling'):
            # know the last played card
            previous_card_info = self.turn.__card_history[-1]
            # print('last played card: ', previous_card_info)
            previous_card_id = previous_card_info[0]
            sel_row1 = int(move.orgn1_row())
            sel_col1 = int(self.turn.colToInt(move.orgn1_col()))
            sel_row2 = int(move.orgn2_row())
            sel_col2 = int(self.turn.colToInt(move.orgn2_col()))
            dest_row = int(move.dRow())
            dest_col = int(self.turn.colToInt(move.dCol()))

            recycling_valid = self.turn.validate_recycling(board_state, move, previous_card_id, self.row_rng, self.col_rng, sel_row1, sel_col1, sel_row2, sel_col2, dest_row, dest_col)
            if recycling_valid:
                move_is_legal = True

        return move_is_legal

    # done
    def gameIsOver(self, state):
        # print('running gameIsOver function')
        winning = self.turn.winCheck(state, self.player)
        if winning == True or self.turn.count() == self.turn.limit():
            return True
        else:
            return  False

    # todo: rework
    def makeMove(self, board_state, move):
        """ Change a board_state object to reflect a player, denoted by color,
            making a move at column 'column'

            Returns a copy of new board_state array with the added move
        """
       # todo: temp deep copy of the board
        temp = copy.deepcopy(board_state)
        # execute the desired move
        if (move.type() == 'regular'):
            card = Card()
            coord = self.turn.initialize_move(card, move)
            self.insert_temp_card(temp, card, coord[0], coord[1], coord[2], coord[3])
        # returned the modified temp board
        return temp

    # based on implemented heuristic
    def value(self, state, objective):
        heuristic = Heuristic(state, objective)
        score = heuristic.evaluate_score()
        # print('score:', score)
        self.en_counter += 1
        return score



    def insert_temp_card(self, board, card, x1, y1, x2, y2):
        if (card.type() == 'horizontal'):
            self.insert_temp_horiz(board, card, x1, y1, x2,
                                      y2)
        if (card.type() == 'vertical'):
            self.insert_temp_vert(board, card, x1, y1, x2,
                                    y2)

    def insert_temp_horiz(self,board, card, x1, y1, x2, y2):
        board.insert(x1, y1, card.left())
        board.insert(x2, y2, card.right())

    def insert_temp_vert(self, board, card, x1, y1, x2, y2):
        board.insert(x1, y1, card.bottom())
        board.insert(x2, y2, card.top())

    def intToColumnLetter(self, col_int):
        str = chr(col_int + 64)
        return str

    def temp_remove_card(self, board, x1, y1, x2, y2):
        temp = copy.deepcopy(board)
        # self.__player.addCard()
        # picked_up = [board.element(x1, y1), board.element(x2, y2)]
        board.clearElement(x1, y1)
        board.clearElement(x2, y2)
        # print('Card Picked Up.')
        # return picked_up
        return temp

    # def alphabeta(node, depth, alpha, beta, role):
    #     if depth = 0 or node is a terminal node then
    #         return the heuristic value of node
    #     if maximizingPlayer then
    #         value := −∞
    #         for each child of node do
    #             value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
    #             α := max(α, value)
    #             if α ≥ β then
    #                 break (* β cut-off *)
    #         return value
    #     else
    #         value := +∞
    #         for each child of node do
    #             value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
    #             β := min(β, value)
    #             if α ≥ β then
    #                 break (* α cut-off *)
    #         return value
