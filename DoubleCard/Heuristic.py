class Heuristic:

    def __init__(self, state, objective):
        self.board_state = state
        self.objective = objective
        if self.objective == 'colors':
            self.role = 'max'
        else:
            self.role = 'min'

    def evaluate_score(self):
        score = 0
        # range stops a x-1
        rng_i = reversed(range(self.board_state.height() + 1))
        rng_j = range(self.board_state.width() + 1)

        sum_We = 0
        sum_Wf = 0
        sum_Re = 0
        sum_Rf = 0
        str_We = ''
        str_Wf = ''
        str_Re = ''
        str_Rf = ''

        for i in rng_i:
            # print ('i = ', i)
            for j in rng_j:
                # print('j = ', j)
                # same row printing
                # print(self.board_state.element(i,j), end='|')
                element = self.board_state.element(i, j)
                position_score = (i - 1) * 10 + j
                if (element == 'W-e'):
                    # print('W-e found at coord: ', i, j)
                    sum_We += position_score
                    str_We += str(position_score) + ' + '
                    # print('score for that position = ', position_score)
                    # get score of coor add it to sum
                if (element == 'W-f'):
                    # print('W-f found at coord: ', i, j)
                    sum_Wf += position_score
                    str_Wf += str(position_score) + ' + '
                if (element == 'R-e'):
                    # print('R-e found at coord: ', i, j)
                    sum_Re += position_score
                    str_Re += str(position_score) + ' + '
                if (element == 'R-f'):
                    # print('R-f found at coord: ', i, j)
                    sum_Rf += position_score
                    str_Rf += str(position_score) + ' + '

        # print('str_We-e = ', str_We)
        # print('sum_W-e = ', sum_We)
        #
        # print('str_Wf =', str_Wf)
        # print('sum_W-f =', sum_Wf)
        #
        # print('str_Re =', str_Re)
        # print('sum_R-e =', sum_Re)
        #
        # print('str_Rf-f =', str_Rf)
        # print('sum_R-f =', sum_Rf)

        score = sum_We + (3 * sum_Wf) - (2 * sum_Rf) - (1.5 * sum_Re)
        # print('e(n) for this board is ', score)
        return score
    # use in game
    # heuristic = Heuristic(self.__board, self.__player.objective())
    # heuristic.evaluate_score()
