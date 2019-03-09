class Board:

    #ctor
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__board = list()

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def insert(self,x, y, content):
        self.__board[x][y] = content

    def element(self,x, y):
        return self.__board[x][y]

    def clearElement(self, x, y):
        self.__board[x][y] = '___'

    def elementToken(self,type, x, y):
        if (self.__board[x][y] != '___' and '-' in self.__board[x][y]):
            tokens = self.__board[x][y].split('-')
            # print('tokens = ', tokens)
            if (type =='color'):
                color = tokens[0]
                return color
            elif (type =='dot'):
                dot = tokens[1]
                return dot
        else: return '_'

    def setBoard(self):
        # for c in ascii_uppercase:
        colHeader = ['  ', ' A ', ' B ', ' C ', ' D ', ' E ', ' F ', ' G ', ' H ']
        self.__board.append(colHeader)

        blankRow = ['___']*(self.__width)

        rng = range (1 , self.__height+1)

        for i in rng:
            emptyRow = [1] + blankRow
            #insert row number
            if len(str(i))<2:
                strI = ' '+str(i)
                emptyRow[0] = strI
            else: emptyRow[0]= str(i)
            self.__board.append(emptyRow)


    def printBoard(self):
        rng_i = reversed(range(len(self.__board)))
        rng_j = range(len(self.__board[0]))

        diplayWidth = (self.__width+1)*4
        rowSeparator = '='*diplayWidth
        print('')
        print(rowSeparator)
        # for each row
        for i in rng_i:
            for j in rng_j:
                # same row printing
                print(self.__board[i][j], end='|')
            print()

        print(rowSeparator)
        print('')

