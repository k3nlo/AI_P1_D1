from pip._vendor.distlib.compat import raw_input
from DoubleCard.Card import Card
from DoubleCard.Move import Move


class Turn:
    def __init__(self, count, board, player, card_history):
        self.__count = count
        self.__board = board
        self.__player = player
        self.__card_history = card_history
        self.__completed = False

    def completed(self):
        return self.__completed

    def start(self):
        # allowed range of moves
        x_rng = range(1, self.__board.height() + 1)
        y_rng = range(1, self.__board.width() + 1)

        while self.__completed != True:
            # usr_input = raw_input('Your regular move: ')
            print(self.__player.name(), end=' ')
            usr_input = raw_input('regular move: ')
            type(usr_input)
            usr_move = usr_input.split()

            if len(usr_move) == 4 and int(usr_move[0]) == 0:
                move = Move('regular', int(usr_move[1]), usr_move[2], usr_move[3])
            # if len(usr_move) == 7:
            #     move = Recycle(usr_move[0], usr_move[1], usr_move[2], usr_move[3], 'recycling', int(usr_move[4]), usr_move[5],
            #                    usr_move[6])

            # move.printMove()

            # process user move
            card = Card()
            card.setPlacement(move.placement())
            # card.printCard()

            # vertical regular move
            if card.type() == 'vertical':
                # bottom
                x1 = int(move.dRow())
                y1 = ord(move.dCol()) - 64
                # top
                x2 = int(move.dRow()) + 1
                y2 = ord(move.dCol()) - 64
            # vertical horizontal move
            if card.type() == 'horizontal':
                # left
                x1 = int(move.dRow())
                y1 = ord(move.dCol()) - 64
                # right
                x2 = int(move.dRow())
                y2 = ord(move.dCol()) - 64 + 1

            # TO-DO: check in block1 and block2 are not out of bound
            if x1 in x_rng and y1 in y_rng and x2 in x_rng and y2 in y_rng:
                # check if card is not floating

                if self.__board.element((x1 - 1), y1) != '__':
                    if card.type() == 'horizontal' and self.__board.element((x2 - 1), y2) != '__':
                        # check if slots are available
                        if self.__board.element(x1, y1) == '__' and self.__board.element(x2, y2) == '__':
                            # insert in board
                            self.__board.insert(x1, y1, card.left())
                            self.__board.insert(x2, y2, card.right())
                            card_info = [card.placement(), x1, y1, x2, y2]
                            self.__card_history.append(card_info)
                            self.__player.subtractCard()
                            self.__completed = True
                        else:
                            print('INVALID MOVE: Slot is not available 1.')
                    elif card.type() == 'vertical':
                        if self.__board.element(x1, y1) == '__' and self.__board.element(x2, y2) == '__':
                            self.__board.insert(x1, y1, card.bottom())
                            self.__board.insert(x2, y2, card.top())
                            card_info = [card.placement(), x1, y1, x2, y2]
                            self.__card_history.append(card_info)
                            self.__player.subtractCard()
                            self.__completed = True
                            # update cards on deck card obj, x1y1, x2y2
                        else:
                            print('INVALID MOVE: Slot is not available 2.')
                    else:
                        print('INVALID MOVE: Floating card 2.')
                else:
                    print('INVALID MOVE: Floating card 1.')
            else:
                print('INVALID MOVE: Out of bound.')

            self.__board.printBoard()
            print('Played cards: ', self.__card_history)
            print(self.__player.name(),' cards left: ', self.__player.cards())
            print()
            if self.__completed:
                break