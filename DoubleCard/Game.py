from numpy.core.defchararray import lower
from pip._vendor.distlib.compat import raw_input
from DoubleCard.Board import Board
from DoubleCard.Player import Player
from DoubleCard.Turn import Turn



class Game:
    def __init__(self, hasWinner, nb_cards, players):
        self.__hasWinner = hasWinner
        self.__nb_cards = nb_cards
        self.__players = players

    def checkResult(self,result):
        if (result):
            self.__hasWinner = result

    @staticmethod
    def main():
        # game starts here
        players = []
        max_nb_cards = 1 # also the limit to regular move
        game = Game(False, max_nb_cards, players)
        objective = ''
        # auto gen for testing
        # game.__players.append(Player('kenlo', 1, game.__nb_cards))
        # game.__players[0].setObjective('colors')
        # game.__players.append(Player('bot', 2, game.__nb_cards))
        # game.__players[1].setObjective('dots')

        for i in range(1, 3):
            msg = 'Player '+ str(i) +' name: '
            usr_input = input(msg)
            name = str(usr_input)
            # new player
            player = Player(name, i, max_nb_cards)
            players.append(player)
            if i == 1:
                while objective != 'colors' or objective != 'dots':
                    msg = 'Player '+ str(i) +' objective (colors or dots): '
                    usr_input = input(msg)
                    objective = str(lower(usr_input))
                    if objective == 'colors' or objective == 'dots':
                        players[i-1].setObjective(objective)
                        break
            else:
               if (players[i-2].objective() == 'colors'): #player 1 at position 0 in list
                   players[i-1].setObjective('dots') #player 2 at position 1 in list
               elif (players[i-2].objective() == 'dots'):
                   players[i-1].setObjective('colors')

        # new blank board
        brd_1 = Board(8,12)
        brd_1.setBoard()
        brd_1.printBoard()

        # cards history
        played_cards = []
        # print(game.__hasWinner)
        turn_count = 0
        end_game = 30
        # regular turns loop
        while game.__hasWinner == False:
            turn_count +=1
            print('Round #',turn_count, sep='')
            print('='*36)
            print('')
            turnP1 = Turn(turn_count, max_nb_cards, end_game, brd_1, players[0], played_cards)
            turnResult = turnP1.start()
            game.checkResult(turnResult)
            if game.__hasWinner:
                break
            turnP2 = Turn(turn_count, max_nb_cards, end_game, brd_1, players[1], played_cards)
            turnResult = turnP2.start()
            game.checkResult(turnResult)
            if game.__hasWinner:
                break
            if turn_count == end_game:
                print('Game Over. It ended in a draw.')
                break
            print('End of Round #', turn_count, sep='')
            print('='*36)
            print('')


# Run the game
Game.main()