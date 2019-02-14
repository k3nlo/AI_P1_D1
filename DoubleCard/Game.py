from pip._vendor.distlib.compat import raw_input

from DoubleCard.Board import Board
from DoubleCard.Card import Card
from DoubleCard.Move import Move
from DoubleCard.Move import Recycle
from DoubleCard.Player import Player


# new players
p1 = Player('kenlo', 1, 12)
p1.setObjective('colors')
p2 = Player('bot', 2, 12)
p1.setObjective('dots')

# new blank board
brd_1 = Board(8,12)
brd_1.setBoard()

# cards on deck
played_cards = []

# allowed range of move
x_rng = range(1, brd_1.height()+1)
y_rng = range(1, brd_1.width()+1)

# For example, the input 0 5 A 2 will indicate that we have a regular move and that card
# will be placed at positions A2 and B2 on the board.



if (p1.cards() > 0):


    usr_input = raw_input('What is your move? ')
    type(usr_input)
    usr_move = usr_input.split()

    if len(usr_move) == 4 and int(usr_move[0])== 0:
        move = Move('regular', int(usr_move[1]), usr_move[2], usr_move[3])
    if len(usr_move) == 7:
        move = Recycle(usr_move[0], usr_move[1], usr_move[2], usr_move[3],'recycling', int(usr_move[4]), usr_move[5], usr_move[6])

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
        y1 =  ord(move.dCol()) - 64
        #right
        x2 = int(move.dRow())
        y2 = ord(move.dCol()) - 64 + 1


    # TO-DO: check in block1 and block2 are not out of bound
    if x1 in x_rng and y1 in y_rng and x2 in x_rng and y2 in y_rng:
        # check if slots are available
        if brd_1.element(x1,y1) == '__' and brd_1.element(x2,y2) == '__':

            # insert in board
            if card.type() == 'horizontal':
                brd_1.insert(x1,y1,card.left())
                brd_1.insert(x2,y2,card.right())
            if card.type() == 'vertical':
                brd_1.insert(x1,y1,card.bottom())
                brd_1.insert(x2,y2,card.top())
            # update cards on deck card obj, x1y1, x2y2
            card_info = [card.placement(), x1, y1, x2, y2]
            played_cards.append(card_info)

            p1.subtractCard()
        else: print('INVALID MOVE: Slot is not available.')
    else: print('INVALID MOVE: Out of bound.')


    brd_1.printBoard()

    print('played cards: ', played_cards)
    print('cards left: ', p1.cards())




# The input F 2 F 3 3 A 2 will indicate that we have a recycling move
# and the card at position F2 F3 will be rotated as
# will be placed at positions A2 and B2 on the board.