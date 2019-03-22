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
import operator
import uuid

from Card import Card
from Heuristic import Heuristic
from DoubleCard.Turn import Turn
from Move import Move

class GameNode(object):
    def __init__(self, board, previous_move=None, current_score=None):
        self.id = uuid.uuid4()
        self.board = board
        if previous_move is None:
            self.previous_move = None
        else:
            self.previous_move = previous_move
        if previous_move is None:
            self.current_score = None
        else:
            self.current_score = current_score

    def getBoard(self):
        return self.board

    def getMove(self):
        return self.previous_move

    def getScore(self):
        return self.current_score

    def getUid(self):
        return self.id

    def setBoard(self, board):
        self.board = board

    def setMove(self, previous_move):
        self.previous_move = previous_move

    def setScore(self, current_score):
        self.current_score = current_score

class StateSpaceSearch(object):
    """ Minimax object that takes  board state
    """
    #todo: board_state is simply a board

    board = None

    # was using tokens x or o , work to be done we have W + R or f + e
    objectives = ['colors', 'dots']

    def __init__(self, alpha_beta, trace, board, player, turn, trace_file=None):
        self.board = copy.deepcopy(board)
        self.row_rng = range(1, self.board.height()+1)
        self.col_rng = range(1, self.board.width()+1)
        self.player = player
        self.turn = turn
        self.en_counter = 0
        self.trace = trace
        self.alpha_beta = alpha_beta
        self.root_depth = player.depth() # TODO: CHANGE SINGLE LEVEL SEARCH
        if trace_file is None:
            self.trace_file = None
        else:
            self.trace_file = trace_file




    def bestMove(self, depth, board_state, curr_player_objective):
        start_time = time.time()
        # print('Starting bestMove() for depth = ', depth)
        if curr_player_objective == self.objectives[0]: # todo: is colors
            player_role = 'max'
            opponent_role = 'min'
        else:
            player_role = 'min'
            opponent_role = 'max'

        print('Bot role is ', player_role)

        # store all legal moves in a key/value dictionnary
        legal_moves = {}  # will map legal move states to their values

        # regular move
        if self.turn.count() <= self.turn.regular_limit():
            start_time2 = time.time()

            self.bot_regular_move(depth, board_state, legal_moves, player_role, opponent_role)

            elapsed_time2 = time.time() - start_time2
            # print('elapsed time bot regular move: ', elapsed_time2)

            # print('legal_moves = ', legal_moves)

            move_list={}

            # todo: process dictionary content
            for uid, game_node in legal_moves.items():
                # print('move = ', game_node.getMove(), 'score =', game_node.getScore())
                move_list[game_node.getMove()] = game_node.getScore()

            best_value = -99999999
            best_move = None
            if (player_role == 'max'):
                key_max_val = max(move_list, key=move_list.get)  # Just use 'min' instead of 'max' for minimum.
                best_move = key_max_val
                best_value = move_list[key_max_val]
                # print('best_move = ', best_move, 'best_value = ' ,best_value)
            if (player_role == 'min'):
                key_min_val = min(move_list, key=move_list.get)  # Just use 'min' instead of 'max' for minimum.
                print(key_min_val, move_list[key_min_val])
                best_move = key_min_val
                best_value = move_list[key_min_val]
                # print('best_move = ', best_move, 'best_value = ', best_value)

            elapsed_time = time.time() - start_time
            print('elapsed time for best move: ', elapsed_time)


        # FIXME: endless remove card loop for recycling moves (card history/playable cards)
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
                            break;

                    elif (card_type == 2 or card_type == 4 or card_type == 6 or card_type == 8):
                        #vertical
                        if (board_state.element(x2+1, y2) == '___'):
                            #card is pickable
                            print('adding:', card)
                            playable_cards.append(card)
                            break;

            print('playable_cards', playable_cards)
            self.bot_recycling_move_new(depth, board_state, playable_cards, legal_moves, player_role, opponent_role)


        if self.trace:
            if self.alpha_beta:
                # file_name = 'traceab'+str(index)+'.txt'
                file_name = 'traceab.txt'
            else:
                # file_name = 'tracemm'+str(index)+'.txt'
                file_name = 'tracemm.txt'
            # file = self.createOutputFile(self.turn.count())
            # file = self.createOutputFile()
            if self.trace_file is None:
                print('Not tracefile to write to.')

            else:
                if ((self.turn.count()) == 1 ):
                    file = open(file_name, "w")
                else:
                    file = open(file_name, "a")
                file.write(str(self.en_counter))
                file.write('\n')
                file.write(str(best_value))
                file.write('\n')
                file.write('\n')
                en_values = list(move_list.values())
                for value in en_values:
                    file.write(str(value))
                    file.write('\n')
                file.write('\n')
                file.close()
        # print('best_move = ', best_move, ', best value = ', best_value)
        # return best_move, best_value
        # print('e(n) was run ', self.en_counter)
        # FIXME: RESET COUNTER OF E(N)
        self.en_counter = 0
        return best_move, best_value


    def bot_regular_move(self,depth, board_state, legal_moves, player_role, opponent_role):
        # ab_legal_moves = []
        print('Running bot regular move:')

        if self.alpha_beta:
            alpha= -99999999
            beta= 99999999
            start_timeab = time.time()
            gameNode = GameNode(board_state)
            best_score_ab = self.alphabeta(depth, gameNode, alpha, beta, player_role, legal_moves)
            print('best alphabeta score = ', best_score_ab)
            elapsed_timeab = time.time() - start_timeab
            # print('elapsed time first alphabeta: ', elapsed_timeab)

        else:
            start_time_mm = time.time()
            gameNode = GameNode(board_state)
            best_score_mm = self.minimax(depth, gameNode, player_role, legal_moves)
            elapsed_timemm = time.time() - start_time_mm
            print('elapsed time first minimax: ', elapsed_timemm)
            print('best minimax score = ', best_score_mm)


    def bot_recycling_move_new(self, depth, board_state, playable_cards, legal_moves, player_role, opponent_role):
        for playable_card in playable_cards:
            # pick it up the card change the state of the board run bot regular move
            x1 = int(playable_card[2])
            y1 = int(playable_card[3])
            x2 = int(playable_card[4])
            y2 = int(playable_card[5])

            # temporaly remove card
            temp_board = self.temp_remove_card(board_state, x1, y1, x2, y2)

            # temp_board.printBoard()
            #
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
            #             # legal_moves[key] = self.minimax(depth - 1, temp, player_role)
            #             legal_moves[key] = self.minimax(depth - 1, temp, player_role)
            # get score
            # in legal moves
            # put it back


    def list_next_legal_states (self, game_node, depth, legal_moves):

        legal_states = []
        # regular move
        # list all playable cells
        playable_cells = []
        for row in self.row_rng:
            # print('trying row', row)
            for col in self.col_rng:
                # print('trying col', col)
                if (game_node.getBoard().element(row, col) == '___' and
                        game_node.getBoard().element(row - 1, col) != '___'):
                    playable_cells.append(str(row) + '-' + str(col))

        # print('playable_cells: ', playable_cells)

        rotation_rng = range(1, 9)
        # in each playable cell check all the card rotation to see which one are legal
        for cell in playable_cells:
            cell_coord = cell.split('-')
            playable_row = cell_coord[0]
            playable_col = self.intToColumnLetter(int(cell_coord[1]))
            # if it is a legal regular move...
            if self.turn.count() <= self.turn.regular_limit():
                for rotation in rotation_rng:
                    # TODO: SAVE THIS MOVE INFO
                    move = Move('regular', rotation, playable_col, playable_row)
                    move_string = str(move.placement()) + '-' + move.dCol() + '-' + move.dRow()

                    if self.isLegalMove(game_node.getBoard(), move):
                        # make the move in column for curr_player
                        # TODO: STORE THIS BOARD/STATE INFO WITH PREVIOUS MOVE + LV 0 OF BOARD EVALUATION
                        temp_state = self.makeMove(game_node.getBoard(), move)
                        new_gameNode = GameNode(temp_state, move_string)
                        legal_states.append(new_gameNode)
                        # insert in hashmap at [key] = value
                        if (depth == self.root_depth):
                            legal_moves[new_gameNode.getUid()] = new_gameNode

        return legal_states

    def minimax(self, depth, game_node, role, legal_moves):
        if (role == 'max'):
            objective = 'colors'
        else:
            objective = 'dots'
        # print('Starting minimax() at depth = ', depth, 'for', role, objective)
        # enumerate all legal moves from this game_node of the board at this level
        # todo: remove duplicate states
        # further state from here

        legal_nodes_list = self.list_next_legal_states(game_node, depth, legal_moves)
        # print('legal moves = ', len(legal_moves))
        # print('legal moves = ', legal_moves)

        # if this node (game_node) is a terminal node or depth == 0...
        if depth == 0 or len(legal_nodes_list) == 0 or self.gameIsOver(game_node.getBoard()):
            # return the heuristic value of node
            score = self.value(game_node.getBoard(), objective)
            game_node.setScore(score)
            return score

        if role == 'max':
            opponent_role = 'min'
            value = -99999999
            for child in legal_nodes_list:
                if child == None:
                    print("child == None (minimax)")
                value = max(value, self.minimax(depth - 1, child, opponent_role, legal_moves))


            # TODO: TAKE INTO CONSIDERATION THE SET DEPTH AT START
            if (depth == (self.root_depth - 1)):
                game_node.setScore(value)
                # print('LV_1 returned value role max = ', value)
            return value

        elif role == 'min':
            opponent_role = 'max'
            value = 99999999
            for child in legal_nodes_list:
                if child == None:
                    print("child == None (minimax)")
                value = min(value, self.minimax(depth - 1, child, opponent_role, legal_moves))


            # TODO: TAKE INTO CONSIDERATION THE SET DEPTH AT START
            if (depth == (self.root_depth - 1)):
                game_node.setScore(value)
                # print('LV_1 returned value role min = ', value)
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


    def gameIsOver(self, state):
        # print('running gameIsOver function')
        # winning = self.turn.winCheck(state, self.player)
        winning = self.turn.silent_winCheck(state, self.player)
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

        # todo: new heuristic
        heuristic = Heuristic(state, objective)
        # score = heuristic.evaluate_score()
        score = heuristic.evaluate_new_score()
        # print('score:', score)
        self.en_counter += 1
        return score


    def notCountedValue(self, state, objective):
        heuristic = Heuristic(state, objective)
        score = heuristic.evaluate_score()
        # print('score:', score)
        # self.en_counter += 1
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

    def alphabeta(self, depth, game_node, alpha, beta, role, legal_moves):
        # if (depth == 1):
        #     print('starting alpha beta with depth = ', depth)
        if (role == 'max'):
            objective = 'colors'
        else:
            objective = 'dots'

        # todo: remove duplicate states
        # list all possible move at this state
        legal_nodes_list = self.list_next_legal_states(game_node, depth, legal_moves)

        if depth == 0 or len(legal_nodes_list) == 0 or self.gameIsOver(game_node.getBoard()):
            # return the heuristic value of node
            score = self.value(game_node.getBoard(), objective)
            game_node.setScore(score)
            return score

        if role == 'max':
            opponent_role = 'min'
            value = -99999999

            for child in legal_nodes_list:
                if child == None:
                    print("child == None (alpha beta)")
                value = max(value, self.alphabeta(depth - 1, child, alpha, beta, opponent_role, legal_moves))
                alpha = max(alpha, value)
                if (alpha >= beta):
                    break
            #TODO: TAKE INTO CONSIDERATION THE SET DEPTH AT START
            if (depth == (self.root_depth-1)):
                game_node.setScore(value)
                # print('LV_1 returned value role max = ', value)
            return value

        elif role == 'min':
            opponent_role = 'max'
            value = 99999999
            for child in legal_nodes_list:
                if child == None:
                    print("child == None (minimax)")
                value = min(value, self.alphabeta(depth - 1, child, alpha, beta, opponent_role, legal_moves))
                beta = min(beta, value)
                if (alpha >= beta):
                    break

            # TODO: TAKE INTO CONSIDERATION THE SET DEPTH AT START
            if (depth == (self.root_depth-1)):
                game_node.setScore(value)
                # print('LV_1 returned value role min = ', value)
            return value
