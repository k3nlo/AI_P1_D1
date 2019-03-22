from pip._vendor.distlib.compat import raw_input
from DoubleCard.Card import Card
from DoubleCard.Move import Move
from DoubleCard.Move import Recycle
import warnings




class Turn:
    def __init__(self, alpha_beta, trace, count, reg_limit, limit, board, player, card_history, trace_file = None):
        self.__count = count
        self.__reg_limit = reg_limit
        self.__limit = limit
        self.__board = board
        self.__player = player
        self.__card_history = card_history
        self.__completed = False
        self.trace = trace
        self.alpha_beta = alpha_beta
        if trace_file is None:
            self.trace_file = None
        else:
            self.trace_file = trace_file

    def count(self):
        return self.__count

    def regular_limit(self):
        return self.__reg_limit

    def card_history(self):
        return self.__card_history

    def limit(self):
        return self.__limit

    def completed(self):
        return self.__completed


    def printHistory (self):
        print('Played Card History', end=': ')
        for cardInfo in self.__card_history:
            print('[ type', cardInfo[1],'in slots:', chr(cardInfo[3]+64), cardInfo[2], '-',chr(cardInfo[5]+64), cardInfo[4],']', end='; ')

        print('')


    def recordMove(self, card, x1, y1, x2, y2):
        card_info = [card.id(), card.placement(), x1, y1, x2, y2]
        self.__card_history.append(card_info)
        self.__player.subtractCard()
        self.__completed = True


    def winCheck(self, board, player):
        # print('running wincheck')
        won = False
        objective = player.objective()
        if (objective == 'colors'):
            # print('checking board for in-line colors')
            tokenOptions = ['R', 'W']
            tokenType = 'color'
        elif (objective == 'dots'):
            # print('checking board for in-line dots')
            tokenOptions = ['f', 'e']
            tokenType = 'dot'
        for token in tokenOptions:
            # vertical check
            # for each row
            # print('checking vertically')
            for row in range(1, (board.height()+1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else: print(row, end='|')

                for col in range(1, (board.width()+1)):
                # same row printing
                #     print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking vertical/column win
                    if (row + 3 <= board.height()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row + 1, col) == token and
                                board.elementToken(tokenType, row + 2, col) == token and
                                board.elementToken(tokenType, row + 3, col) == token):
                            print('vertical win')
                            won = True
                # print()
            # print()

            # horizontal check
            # for each row
            # print('checking horizontally')
            for row in range(1, (board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking horizontal/row win
                    if (col+3 <= board.width()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row, col + 1) == token and
                                board.elementToken(tokenType, row, col + 2) == token and
                                board.elementToken(tokenType, row, col + 3) == token):
                            won = True
                            print('horizontal win')
                # print()
            # print()

            # diagonal check \
            # for each row
            # print('checking diagonally')
            for row in range(1, (board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking diagonal down right win
                    if (col + 3 <= board.width() and row+3 <= board.height()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row + 1, col + 1) == token and
                                board.elementToken(tokenType, row + 2, col + 2) == token and
                                board.elementToken(tokenType, row + 3, col + 3) == token):
                            won = True
                            print('diagonal 1 win')
                # print()
            # print()

            # diagonal check /
            # for each row
            for row in range(1, (board.height() + 1)):
                for col in range(1, (board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking diagonal down left win
                    if (col - 3  >= 1 and row+3 <= board.height()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row + 1, col - 1) == token and
                                board.elementToken(tokenType, row + 2, col - 2) == token and
                                board.elementToken(tokenType, row + 3, col - 3) == token):
                            won = True
                            print('diagonal 2 win')
            #     print()
            # print()
            if (won):
                print('=' * 45)
                print('WE HAVE A REAL WINNER : ', player.name(), 'got 4', token, 'in-line!')
                print('=' * 35)
                return won





    def silent_winCheck(self, board, player):
        # print('running wincheck')
        won = False
        objective = player.objective()
        if (objective == 'colors'):
            # print('checking board for in-line colors')
            tokenOptions = ['R', 'W']
            tokenType = 'color'
        elif (objective == 'dots'):
            # print('checking board for in-line dots')
            tokenOptions = ['f', 'e']
            tokenType = 'dot'
        for token in tokenOptions:
            # vertical check
            # for each row
            for row in range(1, (board.height()+1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else: print(row, end='|')

                for col in range(1, (board.width()+1)):
                # same row printing
                #     print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking vertical/column win
                    if (row + 3 <= board.height()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row + 1, col) == token and
                                board.elementToken(tokenType, row + 2, col) == token and
                                board.elementToken(tokenType, row + 3, col) == token):
                            won = True
                # print()
            # print()

            # horizontal check
            # for each row
            for row in range(1, (board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking horizontal/row win
                    if (col+3 <= board.width()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row, col + 1) == token and
                                board.elementToken(tokenType, row, col + 2) == token and
                                board.elementToken(tokenType, row, col + 3) == token):
                            won = True
                # print()
            # print()

            # diagonal check \
            # for each row
            for row in range(1, (board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking diagonal down right win
                    if (col + 3 <= board.width() and row+3 <= board.height()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row + 1, col + 1) == token and
                                board.elementToken(tokenType, row + 2, col + 2) == token and
                                board.elementToken(tokenType, row + 3, col + 3) == token):
                            won = True
                # print()
            # print()

            # diagonal check /
            # for each row
            for row in range(1, (board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking diagonal down left win
                    if (col - 3  >= 1 and row+3 <= board.height()):
                        if (board.elementToken(tokenType, row, col) == token and
                                board.elementToken(tokenType, row + 1, col - 1) == token and
                                board.elementToken(tokenType, row + 2, col - 2) == token and
                                board.elementToken(tokenType, row + 3, col - 3) == token):
                            won = True
            #     print()
            # print()
            if (won):
                print('=' * 45)
                # print('Silent WINNER : ', player.name(), 'got 4', token, 'in-line!')
                print('=' * 35)
                return won





    def start(self):
        msg_separator = '='*36 + '\n'
        print('It\'s ',self.__player.name(), '\'s turn.', sep = '')
        print(self.__player.name(), ' is playing ', self.__player.objective(),'.', sep = '')
        print('')
        # winning = self.winCheck(self.__board, self.__player)
        # if (winning):
        #     return winning
        # allowed range of moves
        x_rng = range(1, self.__board.height() + 1)
        y_rng = range(1, self.__board.width() + 1)

        msg_separator = '=' * 36 + '\n'
        print(msg_separator)
        print('BOARD AT THE START OF THE TURN')
        # print(msg_separator)
        self.__board.printBoard()


        while self.__completed != True:
            move = None
            # usr_input = raw_input('Your regular move: ')
            if self.__count <= self.__reg_limit:

                if (self.__player.type() == 'ai'):
                    # self is an instance of this turn
                    bot_move = self.__player.move(self.alpha_beta, self.trace, self.__board, self.__player, self, self.trace_file)
                    bot_move_info = bot_move.split('-')
                    move = Move('regular', int(bot_move_info[0]), bot_move_info[1], bot_move_info[2])

                else:
                    print(self.__player.name(), end=' ')
                    usr_input = input('REGULAR move: ')

                    usr_input = str(usr_input).upper()
                    usr_move = usr_input.split()
                    if len(usr_move) == 4 and int(usr_move[0]) == 0:
                        # clear decimal card rotation error and letter
                        rng = range(1, 9)
                        rng_str = ["{:01d}".format(x) for x in rng]
                        if(usr_move[1]) in rng_str:
                            move = Move('regular', int(usr_move[1]), usr_move[2], usr_move[3])
                        else:
                            print(msg_separator)
                            print('INVALID MOVE: non existing card rotation. 1')
                    else:
                        print(msg_separator)
                        print('INVALID MOVE: check your REGULAR move.')



            #fixme: recycling move
            elif (self.__count > self.__reg_limit and self.__count <= self.__limit):

                if (self.__player.type() == 'ai'):
                    # self is an instance of this turn
                    bot_move = self.__player.move(self.alpha_beta, self.trace, self.__board, self.__player, self, self.trace_file )
                    bot_move_info = bot_move.split('-')
                    print('recycling move info:', bot_move_info)
                    print('SORRY, COULDNT FIX THE RECYCLING MOVE IN TIME...')
                    # move = Move('regular', int(bot_move_info[0]), bot_move_info[1], bot_move_info[2])
                    break

                else:
                    print(self.__player.name(), end=' ')
                    usr_input = input('RECYCLING move: ')
                    usr_input = str(usr_input).upper()
                    usr_move = usr_input.split()
                    if len(usr_move) == 7:
                        rng = range(1, 9)
                        rng_str = ["{:01d}".format(x) for x in rng]
                        if (usr_move[4]) in rng_str:
                            move = Recycle(usr_move[0], usr_move[1], usr_move[2], usr_move[3], 'recycling', int(usr_move[4]), usr_move[5],
                                       usr_move[6])
                        else:
                            print(msg_separator)
                            print('INVALID MOVE: non existing card rotation. 2')
                    else:
                        print(msg_separator)
                        print('INVALID MOVE: check your RECYCLING move.')

            if move is not None:
                # move.printMove()

                if (move.type()=='regular'):
                    card = Card()
                    coord = self.initialize_move(card, move)
                    is_valid = self.validate_regular(self.__board, card, x_rng, y_rng, coord[0], coord[1], coord[2], coord[3])
                    if (is_valid):
                        self.insertCard(card, coord[0], coord[1], coord[2], coord[3])


                elif (move.type()=='recycling'):
                    # know the last played card
                    previous_card_info = self.__card_history[-1]
                    print('last played card: ', previous_card_info)
                    previous_card_id = previous_card_info[0]
                    # print('process recycling move here.')
                    # if desired card not last played card
                    sel_row1 = int(move.orgn1_row())
                    sel_col1 = int(self.colToInt(move.orgn1_col()))
                    sel_row2 = int(move.orgn2_row())
                    sel_col2 = int(self.colToInt(move.orgn2_col()))
                    dest_row = int(move.dRow())
                    dest_col = int(self.colToInt(move.dCol()))

                    recylingIsValid = self.validate_recycling(self.__board, move, previous_card_id, x_rng, y_rng, sel_row1, sel_col1, sel_row2, sel_col2, dest_row, dest_col)
                    if (recylingIsValid):
                        self.process_recycling(move, sel_row1, sel_col1, sel_row2, sel_col2)

            # self.__board.printBoard()
            #
            #
            # print(self.__player.name(), ' cards left: ', self.__player.cards())
            # print('')
            # #print('Played cards: ', self.__card_history)
            # self.printHistory()
            # print('_'*36)
            # print('')

            # todo: single test remove
            # self.__completed = True
            if self.__completed:
                break

        print(msg_separator)
        print('BOARD AFTER COMPLETING MOVE')
        # print(msg_separator)
        self.__board.printBoard()

        print(self.__player.name(), ' cards left: ', self.__player.cards())
        print('')
        # print('Played cards: ', self.__card_history)
        self.printHistory()
        print('_' * 36)
        print('')
         # check for a winner

        winning = self.winCheck(self.__board, self.__player)
        if (winning):
            return winning


    def validate_regular(self, board, card, x_rng, y_rng, x1, y1, x2, y2):
        msg_separator = '='*36 +'\n'
        valid_move = False
        # Move Validity Check
        if x1 in x_rng and y1 in y_rng and x2 in x_rng and y2 in y_rng:
            # check if card 1st element is not floating
            if board.element((x1 - 1), y1) != '___':
                # check if card 2nd element is not floating
                if card.type() == 'horizontal' and board.element((x2 - 1), y2) != '___':
                    # check if slots are available
                    if board.element(x1, y1) == '___' and board.element(x2, y2) == '___':
                        valid_move = True
                        # insert in board
                    else:
                        print(msg_separator)
                        print('INVALID MOVE: Slot is not available 1.')
                elif card.type() == 'vertical':
                    # check if slots are available
                    if board.element(x1, y1) == '___' and board.element(x2, y2) == '___':
                        valid_move = True

                    else:
                        print(msg_separator)
                        print('INVALID MOVE: Slot is not available 2.')
                else:
                    print(msg_separator)
                    print('INVALID MOVE: Floating card 2.')
            else:
                print(msg_separator)
                print('INVALID MOVE: Floating card 1.')
        else:
            print(msg_separator)
            print('INVALID MOVE: Out of bound.')

        return valid_move


    def bot_validate_regular(self, board, card, x_rng, y_rng, x1, y1, x2, y2):
        msg_separator = '='*36 +'\n'
        valid_move = False
        # Move Validity Check
        if x1 in x_rng and y1 in y_rng and x2 in x_rng and y2 in y_rng:
            # check if card 1st element is not floating
            if board.element((x1 - 1), y1) != '___':
                # check if card 2nd element is not floating
                if card.type() == 'horizontal' and board.element((x2 - 1), y2) != '___':
                    # check if slots are available
                    if board.element(x1, y1) == '___' and board.element(x2, y2) == '___':
                        valid_move = True
                        # insert in board
                    # else:
                        # print(msg_separator)
                        # print('INVALID MOVE: Slot is not available 1.')
                elif card.type() == 'vertical':
                    # check if slots are available
                    if board.element(x1, y1) == '___' and board.element(x2, y2) == '___':
                        valid_move = True

        #             else:
        #                 print(msg_separator)
        #                 print('INVALID MOVE: Slot is not available 2.')
        #         else:
        #             print(msg_separator)
        #             print('INVALID MOVE: Floating card 2.')
        #     else:
        #         print(msg_separator)
        #         print('INVALID MOVE: Floating card 1.')
        # else:
        #     print(msg_separator)
        #     print('INVALID MOVE: Out of bound.')

        return valid_move


    def validate_recycling(self,board, move, previous_card_id, row_rng, col_rng, org_row1, org_col1, org_row2, org_col2, dest_row, dest_col):
        msg_separator = '=' * 36 + '\n'
        valid_recycling = False
        # get the desired card
        print('Searching for desired card: ', org_row1, org_col1, org_row2, org_col2)
        desired_id = None

        for card in self.__card_history:
            x1 = int(card[2])
            y1 = int(card[3])
            x2 = int(card[4])
            y2 = int(card[5])
            if (org_row1 == x1 and org_col1 == y1 and org_row2 == x2 and org_col2 == y2):
                print('Found desired card:', card)
                found_card = card
                desired_id = card[0]
                if (desired_id != previous_card_id):
                    # validate removal is allowed and remove
                    desType = int(card[1])
                    if (desType == 1 or desType == 3 or desType == 5 or desType == 7):
                        # horizontal
                        if (board.element(org_row1 + 1, org_col1) == '___'
                                and board.element(org_row2 + 1, org_col2) == '___'):
                            # clear space
                            picked_content = self.pickUpCard(org_row1, org_col1, org_row2, org_col2)
                            # different position
                            if (dest_row != x1 or dest_col != y1):
                                new_card = Card()
                                coord = self.initialize_move(new_card, move)
                                is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1], coord[2],
                                                                 coord[3])
                                if (is_valid):
                                    valid_recycling = True

                                self.putHorizontalCardBack(picked_content[0], picked_content[1], org_row1, org_col1,
                                                            org_row2, org_col2)
                                break

                            # same position different rotation
                            elif (dest_row == x1 and dest_col == y1):
                                if (move.placement() != desType):
                                    new_card = Card()
                                    coord = self.initialize_move(new_card, move)
                                    is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1],
                                                                     coord[2],
                                                                     coord[3])
                                    if (is_valid):
                                        valid_recycling = True

                                    # put it back
                                    self.putHorizontalCardBack(picked_content[0], picked_content[1],
                                                                   org_row1, org_col1, org_row2, org_col2)
                                    break

                                if (move.placement() == desType):
                                    print(msg_separator)
                                    print('INVALID MOVE: you are supposed to change position and/or rotation 1')
                                    self.putHorizontalCardBack(picked_content[0], picked_content[1],
                                                               org_row1, org_col1, org_row2, org_col2)
                                    break
                        else:
                            print(msg_separator)
                            print('INVALID MOVE: Card can not be picked up. 1')

                    elif (desType == 2 or desType == 4 or desType == 6 or desType == 8):

                        # vertical removal after insertion
                        if board.element(org_row2 + 1, org_col2) == '___':  # nothing on top
                            # clear space
                            picked_content = self.pickUpCard(org_row1, org_col1, org_row2, org_col2)
                            print('picked up = ', picked_content)
                            # 0 bottom
                            # 1 top
                            # different position
                            if (dest_row != x1 or dest_col != y1):
                                new_card = Card()
                                coord = self.initialize_move(new_card, move)
                                is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1], coord[2],
                                                                 coord[3])
                                if (is_valid):
                                    valid_recycling = True

                                # put it back
                                self.putVerticalCardBack(picked_content[0], picked_content[1], org_row1, org_col1, org_row2, org_col2)
                                break


                            # same position different rotation
                            elif (dest_row == x1 and dest_col == y1):
                                if (move.placement() != desType):
                                    new_card = Card()
                                    coord = self.initialize_move(new_card, move)
                                    is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1],
                                                                     coord[2],
                                                                     coord[3])
                                    if (is_valid):
                                        valid_recycling = True

                                    # put it back
                                    self.putVerticalCardBack(picked_content[0], picked_content[1],
                                                                 org_row1, org_col1, org_row2, org_col2)
                                    break

                                if (move.placement() == desType):
                                    print(msg_separator)
                                    print('INVALID MOVE: you are supposed to change position and/or rotation 2')
                                    self.putVerticalCardBack(picked_content[0], picked_content[1], org_row1, org_col1, org_row2, org_col2)
                                    break
                        else:
                            print(msg_separator)
                            print('INVALID MOVE: Card can not be picked up. 2')

                elif (desired_id == previous_card_id):
                    print(msg_separator)
                    print('INVALID MOVE: Can not re-play this card.')
                    break

        if desired_id == None:
            print(msg_separator)
            print('INVALID MOVE: Not a playable card.')

        return valid_recycling


    def bot_validate_recycling(self,board, move, previous_card_id, row_rng, col_rng, org_row1, org_col1, org_row2, org_col2, dest_row, dest_col):
        msg_separator = '=' * 36 + '\n'
        valid_recycling = False
        # get the desired card
        print('Searching for desired card: ', org_row1, org_col1, org_row2, org_col2)
        desired_id = None

        for card in self.__card_history:
            x1 = int(card[2])
            y1 = int(card[3])
            x2 = int(card[4])
            y2 = int(card[5])
            if (org_row1 == x1 and org_col1 == y1 and org_row2 == x2 and org_col2 == y2):
                print('Found desired card:', card)
                found_card = card
                desired_id = card[0]
                if (desired_id != previous_card_id):
                    # validate removal is allowed and remove
                    desType = int(card[1])
                    if (desType == 1 or desType == 3 or desType == 5 or desType == 7):
                        # horizontal
                        if (board.element(org_row1 + 1, org_col1) == '___'
                                and board.element(org_row2 + 1, org_col2) == '___'):
                            # clear space
                            picked_content = self.pickUpCard(org_row1, org_col1, org_row2, org_col2)
                            # different position
                            if (dest_row != x1 or dest_col != y1):
                                new_card = Card()
                                coord = self.initialize_move(new_card, move)
                                is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1], coord[2],
                                                                 coord[3])
                                if (is_valid):
                                    valid_recycling = True

                                self.putHorizontalCardBack(picked_content[0], picked_content[1], org_row1, org_col1,
                                                            org_row2, org_col2)
                                break

                            # same position different rotation
                            elif (dest_row == x1 and dest_col == y1):
                                if (move.placement() != desType):
                                    new_card = Card()
                                    coord = self.initialize_move(new_card, move)
                                    is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1],
                                                                     coord[2],
                                                                     coord[3])
                                    if (is_valid):
                                        valid_recycling = True

                                    # put it back
                                    self.putHorizontalCardBack(picked_content[0], picked_content[1],
                                                                   org_row1, org_col1, org_row2, org_col2)
                                    break

                                if (move.placement() == desType):
                                    print(msg_separator)
                                    print('INVALID MOVE: you are supposed to change position and/or rotation 1')
                                    self.putHorizontalCardBack(picked_content[0], picked_content[1],
                                                               org_row1, org_col1, org_row2, org_col2)
                                    break
                        else:
                            print(msg_separator)
                            print('INVALID MOVE: Card can not be picked up. 1')

                    elif (desType == 2 or desType == 4 or desType == 6 or desType == 8):

                        # vertical removal after insertion
                        if board.element(org_row2 + 1, org_col2) == '___':  # nothing on top
                            # clear space
                            picked_content = self.pickUpCard(org_row1, org_col1, org_row2, org_col2)
                            print('picked up = ', picked_content)
                            # 0 bottom
                            # 1 top
                            # different position
                            if (dest_row != x1 or dest_col != y1):
                                new_card = Card()
                                coord = self.initialize_move(new_card, move)
                                is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1], coord[2],
                                                                 coord[3])
                                if (is_valid):
                                    valid_recycling = True

                                # put it back
                                self.putVerticalCardBack(picked_content[0], picked_content[1], org_row1, org_col1, org_row2, org_col2)
                                break


                            # same position different rotation
                            elif (dest_row == x1 and dest_col == y1):
                                if (move.placement() != desType):
                                    new_card = Card()
                                    coord = self.initialize_move(new_card, move)
                                    is_valid = self.validate_regular(board, new_card, row_rng, col_rng, coord[0], coord[1],
                                                                     coord[2],
                                                                     coord[3])
                                    if (is_valid):
                                        valid_recycling = True

                                    # put it back
                                    self.putVerticalCardBack(picked_content[0], picked_content[1],
                                                                 org_row1, org_col1, org_row2, org_col2)
                                    break

                                if (move.placement() == desType):
                                    print(msg_separator)
                                    print('INVALID MOVE: you are supposed to change position and/or rotation 2')
                                    self.putVerticalCardBack(picked_content[0], picked_content[1], org_row1, org_col1, org_row2, org_col2)
                                    break
                        else:
                            print(msg_separator)
                            print('INVALID MOVE: Card can not be picked up. 2')

                elif (desired_id == previous_card_id):
                    print(msg_separator)
                    print('INVALID MOVE: Can not re-play this card.')
                    break

        if desired_id == None:
            print(msg_separator)
            print('INVALID MOVE: Not a playable card.')

        return valid_recycling


    def process_recycling(self,move, org_row1, org_col1, org_row2, org_col2):
        # find card in history
        for card in self.__card_history:
            x1 = int(card[2])
            y1 = int(card[3])
            x2 = int(card[4])
            y2 = int(card[5])
            if (org_row1 == x1 and org_col1 == y1 and org_row2 == x2 and org_col2 == y2):
                # print('Found desired card:', card)
                found_card = card
        # remove card from board
        picked_card = self.pickUpCard(org_row1, org_col1, org_row2, org_col2)
        # user + 1 card
        self.__card_history.remove(found_card)
        new_card = Card()
        # user -1 card
        coord = self.initialize_move(new_card, move)
        self.insertCard(new_card, coord[0], coord[1], coord[2], coord[3])


    def insertCard(self, card, x1, y1, x2, y2):
        if (card.type() == 'horizontal'):
            self.insertHorizontalCard(card, x1, y1, x2,
                                      y2)
        if (card.type() == 'vertical'):
            self.insertVerticalCard(card, x1, y1, x2,
                                      y2)


    def insertHorizontalCard(self, card, x1, y1, x2, y2):
        self.__board.insert(x1, y1, card.left())
        self.__board.insert(x2, y2, card.right())
        self.recordMove(card, x1, y1, x2, y2)


    def insertVerticalCard(self, card, x1, y1, x2, y2):
        self.__board.insert(x1, y1, card.bottom())
        self.__board.insert(x2, y2, card.top())
        self.recordMove(card, x1, y1, x2, y2)


    def colToInt(self, column):
        intVal = ord(column) - 64
        return int(intVal)


    def initialize_move(self, card, move):
        # process user move

        card.setPlacement(move.placement())
        # card.printCard()

        # vertical regular move
        if card.type() == 'vertical':
            # bottom
            x1 = int(move.dRow())
            y1 = self.colToInt(move.dCol())
            # top
            x2 = int(move.dRow()) + 1
            y2 = self.colToInt(move.dCol())
        #  horizontal move
        if card.type() == 'horizontal':
            # left
            x1 = int(move.dRow())
            y1 = self.colToInt(move.dCol())
            # right
            x2 = int(move.dRow())
            y2 = self.colToInt(move.dCol()) + 1
        destination = [x1, y1, x2, y2]
        return destination


    def pickUpCard(self, x1, y1, x2, y2):
        self.__player.addCard()
        picked_up = [ self.__board.element(x1, y1), self.__board.element(x2, y2)]
        self.__board.clearElement(x1, y1)
        self.__board.clearElement(x2, y2)
        print('Card Picked Up.')
        return picked_up


    def putHorizontalCardBack(self, leftContent,rightContent , x1, y1, x2, y2):
        self.__board.insert(x1, y1, leftContent)
        self.__board.insert(x2, y2, rightContent)
        self.__player.subtractCard()


    def putVerticalCardBack(self, bottomContent, topContent, x1, y1, x2, y2):
        self.__board.insert(x1, y1, bottomContent) # bottom
        self.__board.insert(x2, y2, topContent) # top
        self.__player.subtractCard()
