class Move(object):

    #ctor
    def __init__(self, type, placement, dCol, dRow):
        #rotation number
        self.__type = type
        self.__placement = placement
        self.__dCol = dCol
        self.__dRow = dRow

    def printMove(self):
        print(
            'type: ', self.__type)
        print(
            'placement: ', self.__placement)
        print(
            'destination: ', self.__dCol,self.__dRow
        )

    def placement(self):
        return self.__placement
    def dCol(self):
        return self.__dCol
    def dRow(self):
        return self.__dRow

class Recycle(Move):
    def __init__(self, orgn1_col, orgn1_row, orng2_col, orgn2_row, *args, **kwargs):
        self.__orgn1_col = orgn1_col
        self.__orgn1_row = orgn1_row
        self.__orng2_col = orng2_col
        self.__orgn2_row = orgn2_row
        super(Recycle, self).__init__(*args, **kwargs)

    def printMove(self):
        print('origin: ', self.__orgn1_col, self.__orgn1_row, self.__orng2_col, self.__orgn2_row)
        super(Recycle,self).printMove()

