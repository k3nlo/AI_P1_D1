from DoubleCard.Board import Board
from DoubleCard.Player import Player
from DoubleCard.Turn import Turn



# new players
p1 = Player('kenlo', 1, 2)
p1.setObjective('colors')
p2 = Player('bot', 2, 2)
p1.setObjective('dots')

# new blank board
brd_1 = Board(8,12)
brd_1.setBoard()

# cards history
played_cards = []

noWinner = True
turnCount = 0
# regular turns loop
while noWinner:
  turnCount +=1
  print('Turn #',turnCount)
  turnP1 = Turn(turnCount, brd_1, p1, played_cards)
  turnP1.start()
  turnP2 = Turn(turnCount, brd_1, p2, played_cards)
  turnP2.start()
  if noWinner == False or p2.cards()==0 :
    break











# The input F 2 F 3 3 A 2 will indicate that we have a recycling move
# and the card at position F2 F3 will be rotated as
# will be placed at positions A2 and B2 on the board.