from pip._vendor.distlib.compat import raw_input
from DoubleCard.Card import Card
from DoubleCard.Move import Move
from DoubleCard.Move import Recycle
import warnings


class Turn:
    def __init__(self, count, limit, board, player, card_history):
        self.__count = count
        self.__limit = limit
        self.__board = board
        self.__player = player
        self.__card_history = card_history
        self.__completed = False

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


    def winCheck(self):
        won = False
        objective = self.__player.objective()
        print(self.__player.name(),' is playing ',self.__player.objective())

        if (objective == 'colors'):
            print('checking board for in-line colors')
            tokenOptions = ['R', 'W']
            tokenType = 'color'
        elif (objective == 'dots'):
            print('checking board for in-line dots')
            tokenOptions = ['f', 'e']
            tokenType = 'dot'
        for token in tokenOptions:
            # vertical check
            # for each row
            for row in range(1, (self.__board.height()+1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else: print(row, end='|')

                for col in range(1, (self.__board.width()+1)):
                # same row printing
                #     print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking vertical/column win
                    if (self.__board.elementToken(tokenType, row, col) == token and
                            self.__board.elementToken(tokenType, row + 1, col) == token and
                            self.__board.elementToken(tokenType, row + 2, col) == token and
                            self.__board.elementToken(tokenType, row + 3, col) == token):
                        won = True
                # print()
            # print()

            # horizontal check
            # for each row
            for row in range(1, (self.__board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (self.__board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking horizontal/row win
                    if (self.__board.elementToken(tokenType, row, col) == token and
                            self.__board.elementToken(tokenType, row, col + 1) == token and
                            self.__board.elementToken(tokenType, row, col + 2) == token and
                            self.__board.elementToken(tokenType, row, col + 3) == token):
                        won = True
                # print()
            # print()

            # diagonal check \
            # for each row
            for row in range(1, (self.__board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (self.__board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking horizontal/row win
                    if (self.__board.elementToken(tokenType, row, col) == token and
                            self.__board.elementToken(tokenType, row + 1, col + 1) == token and
                            self.__board.elementToken(tokenType, row + 2, col + 2) == token and
                            self.__board.elementToken(tokenType, row + 3, col + 3) == token):
                        won = True
                # print()
            # print()

            # diagonal check /
            # for each row
            for row in range(1, (self.__board.height() + 1)):
                # if len(str(row)) == 1:
                #     print('', row, end='|')
                # else:
                #     print(row, end='|')
                for col in range(1, (self.__board.width() + 1)):
                    # print(self.__board.elementToken(tokenType, row, col), end='|')
                    # checking horizontal/row win
                    if (self.__board.elementToken(tokenType, row, col) == token and
                            self.__board.elementToken(tokenType, row + 1, col - 1) == token and
                            self.__board.elementToken(tokenType, row + 2, col - 2) == token and
                            self.__board.elementToken(tokenType, row + 3, col - 3) == token):
                        won = True
            #     print()
            # print()
            if(won):
                print(self.__player.name(), 'got 4', token, 'in-line.')
                return won



    def start(self):
        # real is 12
        regular_move = 12
        winning = self.winCheck()
        if (winning):
            return winning
        # allowed range of moves
        x_rng = range(1, self.__board.height() + 1)
        y_rng = range(1, self.__board.width() + 1)

        while self.__completed != True:
            # usr_input = raw_input('Your regular move: ')
            if self.__count <= regular_move:
                print(self.__player.name(), end=' ')
                usr_input = input('regular move: ')
                usr_input = str(usr_input).upper()
                usr_move = usr_input.split()
                if len(usr_move) == 4 and int(usr_move[0]) == 0:
                    move = Move('regular', int(usr_move[1]), usr_move[2], usr_move[3])
                else:
                    print('INVALID MOVE: check your regular move syntax.')

            elif (self.__count > regular_move and self.__count <= self.__limit):
                print(self.__player.name(), end=' ')
                usr_input = input('recycling move: ')
                usr_input = str(usr_input).upper()
                usr_move = usr_input.split()
                if len(usr_move) == 7:
                    move = Recycle(usr_move[0], usr_move[1], usr_move[2], usr_move[3], 'recycling', int(usr_move[4]), usr_move[5],
                                   usr_move[6])
                else:
                    print('INVALID MOVE: check your recycling move syntax.')


            move.printMove()

            if (move.type()=='regular'):
                card = Card()
                coord = self.simpleMove(card, move)
                self.validateMove(card, x_rng, y_rng, coord[0], coord[1], coord[2], coord[3])

            elif (move.type()=='recycling'):
                # know the last played card
                previous_card_info = self.__card_history[-1]
                previous_card_id = previous_card_info[0]
                print('process recycling move here.')
                # if desired card not last played card
                sel_row1 = int(move.orgn1_row())
                sel_col1 = int(self.colToInt(move.orgn1_col()))
                sel_row2 = int(move.orgn2_row())
                sel_col2 = int(self.colToInt(move.orgn2_col()))
                dest_row = int(move.dRow())
                dest_col = int(self.colToInt(move.dCol()))

                # get the desired card
                print('Searching for desired card: ', sel_row1, sel_col1, sel_row2, sel_col2)
                for card in self.__card_history:
                    x1 = int(card[2])
                    y1 = int(card[3])
                    x2 = int(card[4])
                    y2 = int(card[5])
                    if (sel_row1 == x1 and sel_col1 == y1 and sel_row2 == x2 and sel_col2 == y2):
                        print('Found desired card:', card)
                        desId = card[0]
                        if(desId!= previous_card_id):
                            # validate removal is allowed and remove
                            desType = int(card[1])
                            if(desType == 1 or desType == 3 or desType == 5 or desType == 7):
                                # horizontal removal
                                if (self.__board.element(sel_row1 + 1, sel_col1) == '___'
                                        and self.__board.element(sel_row2 + 1, sel_col2)  == '___'):
                                    self.__card_history.remove(card)
                                    self.__board.clearElement(sel_row1, sel_col1)
                                    self.__board.clearElement(sel_row2, sel_col2)
                                    print('Horizontal Card Deleted.')
                                    # different position
                                    if (dest_row != x1  or dest_col != y1):
                                        card = Card()
                                        coord = self.simpleMove(card, move)
                                        self.validateMove(card, x_rng, y_rng, coord[0], coord[1], coord[2], coord[3])
                                    elif (dest_row == x1 and dest_col == y1):
                                        if (move.placement() != desType):
                                            card = Card()
                                            coord = self.simpleMove(card, move)
                                            self.validateMove(card, x_rng, y_rng, coord[0], coord[1], coord[2],
                                                              coord[3])
                                    else: print('INVALID MOVE: you are supposed to change placement or position')
                            elif(desType == 2 or desType == 4 or desType == 6 or desType == 8):
                                # vertical removal
                                if self.__board.element(sel_row2 + 1, sel_col2) == '___':
                                    self.__card_history.remove(card)
                                    self.__board.clearElement(sel_row1, sel_col1)
                                    self.__board.clearElement(sel_row2, sel_col2)
                                    print('Vertical Card Deleted.')
                                    # different position
                                    if (dest_row != x1 or dest_col != y1):
                                        card = Card()
                                        coord = self.simpleMove(card, move)
                                        self.validateMove(card, x_rng, y_rng, coord[0], coord[1], coord[2], coord[3])
                                    elif (dest_row == x1 and dest_col == y1):
                                        if (move.placement() != desType):
                                            card = Card()
                                            coord = self.simpleMove(card, move)
                                            self.validateMove(card, x_rng, y_rng, coord[0], coord[1], coord[2],
                                                              coord[3])
                                    else: print('INVALID MOVE: you are supposed to change placement or position')
                        else: print('INVALID MOVE: Can not re play this card.')
                    else: print('Desired Card not found.')


                # validate move and place on boardf





            self.__board.printBoard()

            #print('Played cards: ', self.__card_history)
            self.printHistory()

            print(self.__player.name(),' cards left: ', self.__player.cards())
            print()
            if self.__completed:
                break
         # check for a winner
        winning = self.winCheck()
        if (winning):
            return winning

    def validateMove(self, card, x_rng, y_rng, x1, y1, x2, y2):
        # Move Validity Check
        if x1 in x_rng and y1 in y_rng and x2 in x_rng and y2 in y_rng:
            # check if card 1st element is not floating
            if self.__board.element((x1 - 1), y1) != '___':
                # check if card 2nd element is not floating
                if card.type() == 'horizontal' and self.__board.element((x2 - 1), y2) != '___':
                    # check if slots are available
                    if self.__board.element(x1, y1) == '___' and self.__board.element(x2, y2) == '___':
                        # insert in board
                        self.__board.insert(x1, y1, card.left())
                        self.__board.insert(x2, y2, card.right())
                        self.recordMove(card, x1, y1, x2, y2)
                    else:
                        print('INVALID MOVE: Slot is not available 1.')
                elif card.type() == 'vertical':
                    # check if slots are available
                    if self.__board.element(x1, y1) == '___' and self.__board.element(x2, y2) == '___':
                        self.__board.insert(x1, y1, card.bottom())
                        self.__board.insert(x2, y2, card.top())
                        self.recordMove(card, x1, y1, x2, y2)
                    else:
                        print('INVALID MOVE: Slot is not available 2.')
                else:
                    print('INVALID MOVE: Floating card 2.')
            else:
                print('INVALID MOVE: Floating card 1.')
        else:
            print('INVALID MOVE: Out of bound.')

    def colToInt(self, column):
        intVal = ord(column) - 64
        return int(intVal)

    def simpleMove(self, card, move):
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
        # vertical horizontal move
        if card.type() == 'horizontal':
            # left
            x1 = int(move.dRow())
            y1 = self.colToInt(move.dCol())
            # right
            x2 = int(move.dRow())
            y2 = self.colToInt(move.dCol()) + 1
        destination = [x1, y1, x2, y2]
        return destination
