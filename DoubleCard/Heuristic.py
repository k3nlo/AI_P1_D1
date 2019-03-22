class Heuristic:

    def __init__(self, state, objective):
        self.board_state = state
        self.objective = objective
        # if self.objective == 'colors':
        #     self.role = 'max'
        # else:
        #     self.role = 'min'

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

    def evaluate_new_score(self):

        if self.objective == 'colors':
            tokenType= 'color'
            tokens = ['R', 'W']
            op_tokens = ['e', 'f']
            op_tokenType = 'dot'
            # tokens are R or W
        else:
            tokenType = 'dot'
            tokens = ['e', 'f']
            op_tokens = ['R', 'W']
            op_tokenType = 'color'



        my_fours_tk1 = self.checkForStreak(self.board_state, tokens[0], 4, tokenType)
        my_threes_tk1 = self.checkForStreak(self.board_state, tokens[0], 3, tokenType)
        my_twos_tk1 = self.checkForStreak(self.board_state, tokens[0], 2, tokenType)

        tk1_score =  1000*my_fours_tk1 + 100*my_threes_tk1 + 10*my_twos_tk1

        my_fours_tk2 = self.checkForStreak(self.board_state, tokens[1], 4, tokenType)
        my_threes_tk2 = self.checkForStreak(self.board_state, tokens[1], 3, tokenType)
        my_twos_tk2 = self.checkForStreak(self.board_state, tokens[1], 4, tokenType)

        tk2_score = 1000*my_fours_tk2 + 100*my_threes_tk2 + 10*my_twos_tk2

        op_fours_tk1 = self.checkForStreak(self.board_state, op_tokens[0], 4, op_tokenType)
        op_threes_tk1 = self.checkForStreak(self.board_state, op_tokens[0], 3, op_tokenType)
        op_twos_tk1 = self.checkForStreak(self.board_state, op_tokens[0], 2, op_tokenType)

        tk1_op_score = 1000*op_fours_tk1 + 100*op_threes_tk1 + 10*op_twos_tk1

        op_fours_tk2 = self.checkForStreak(self.board_state, op_tokens[1], 4, op_tokenType)
        op_threes_tk2 = self.checkForStreak(self.board_state, op_tokens[1], 3, op_tokenType)
        op_twos_tk2 = self.checkForStreak(self.board_state, op_tokens[1], 4, op_tokenType)

        tk2_op_score = 1000*op_fours_tk2 + 100*op_threes_tk2 + 10*op_twos_tk2

        score = tk1_score + 2*tk2_score - 1.5*tk1_op_score - 2.5*tk2_op_score

        return score

    def checkForStreak(self, board_state, token, streak_length, tokenType):
        count = 0
        rng_i = reversed(range(self.board_state.height() + 1))
        rng_j = range(self.board_state.width() + 1)
        for i in rng_i:
            # print ('i = ', i)
            for j in rng_j:
                # get cell  token
                element = board_state.elementToken(tokenType, i, j)
                if (element == token):
                    # check if a vertical streak_length starts at (i, j)
                    count += self.verticalStreak(i, j, board_state, streak_length, token, tokenType)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, board_state, streak_length, token, tokenType)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, board_state, streak_length, token, tokenType)

        # return the sum of streaks of length 'streak_length'
        return count

    def verticalStreak(self, row, col, board_state, streak_length, token, tokenType):

        consecutiveCount = 0
            # vertical check
        for row_i in range(row, (board_state.height() + 1)):
            if (board_state.elementToken(tokenType, row_i, col) == token):
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak_length:
            return 1
        else:
            return 0

    def horizontalStreak(self, row, col, board_state, streak_length, token, tokenType):
        consecutiveCount = 0
        for col_j in range(col, (board_state.width() + 1)):
            if (board_state.elementToken(tokenType, row, col_j) == token):
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak_length:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, col, board_state, streak_length, token, tokenType):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0


        # diagonal check /
        max_row = 12
        max_col = 8
        col_j = col
        for row_i in range(row, max_row+1):
            if col_j > (max_col):
                break
            elif (board_state.elementToken(tokenType, row_i, col_j) == token):
                consecutiveCount += 1
            else:
                break
            col_j += 1  # increment column when row is incremented


        if consecutiveCount >= streak_length:
            total += 1

        col_j = col
        for row_i in range(row, 0, -1):
            if col_j > (max_col):
                break
            elif (board_state.elementToken(tokenType, row_i, col_j) == token):
                consecutiveCount += 1
            else:
                break
            col_j += 1  # increment column when row is incremented


        if consecutiveCount >= streak_length:
            total += 1

        return total



























        return total


    # use in game
    # heuristic = Heuristic(self.__board, self.__player.objective())
    # heuristic.evaluate_score()
