from DoubleCard.StateSpaceSearch import StateSpaceSearch


class Player(object):
    def __init__(self, name, number, cards, type):
        # rotation number
        self.__name = name
        self.__number = number
        self.__objective = ''
        self.__cards = cards
        self.__type = type

    def name(self):
        return self.__name
    def number(self):
        return self.__number
    def objective(self):
        return self.__objective
    def cards(self):
        return self.__cards
    def setObjective(self, objective):
        self.__objective = objective

    def subtractCard(self):
        self.__cards-=1
    def addCard(self):
        self.__cards+=1

    def type(self):
        return self.__type


class AIPlayer(Player):
    def __init__(self, depth, *args, **kwargs):
        self.__depth = depth
        super(AIPlayer, self).__init__(*args, **kwargs)

    def depth(self):
        return  self.__depth

    def move(self, alpha_beta, trace, board_state, player, turn, trace_file):
        # print(player.name(), 'is playing the', player.objective())

        # sleeping for about 1 second makes it looks like he's thinking
        # time.sleep(random.randrange(8, 17, 1)/10.0)
        # return random.randint(0, 6)

        stateSearch = StateSpaceSearch(alpha_beta, trace, board_state, player, turn, trace_file)
        # print('Ignore all bots move for now')
        # m.gameIsOver(turn)
        # best_move, value = minimax.bestMove(self.__depth, board_state, self.__objective)
        print('Bot Starting BestMove()')
        # minimax.bestMove(self.__depth, board_state, player.objective())
        best_move, value = stateSearch.bestMove(self.__depth, board_state, player.objective())
        # value = stateSearch.bestMove(self.__depth, board_state, player.objective())
        msg_separator = '=' * 36 + '\n'
        print(msg_separator)
        print('BEST MOVE: 0-', best_move, 'value =', value)
        print(msg_separator)
        # print('Best value =', value)
        return best_move