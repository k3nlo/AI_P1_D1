import uuid
class Card:

    #ctor
    def __init__(self):
        #rotation number
        self.__uid = uuid.uuid4()
        self.__placement = 0
        self.__type = ''
        # top
        self.__tBlock = ''
        # bottom
        self.__bBlock = ''
        # left
        self.__lBlock = ''
        # right
        self.__rBlock = ''

    def placement(self):
        return self.__placement
    def type(self):
        return self.__type
    def top(self):
        return self.__tBlock
    def bottom(self):
        return self.__bBlock
    def left(self):
        return self.__lBlock
    def right(self):
        return self.__rBlock

    def id(self):
        return self.__uid

    def setPlacement(self, placement):
        self.__placement = placement
        # type according to rotation
        if placement % 2 == 0:
            self.__type = 'vertical'
            self.setBlock()
        else:
            self.__type = 'horizontal'
            self.setBlock()
        self.setBlock()


    def setBlock(self):
        if self.__placement == 1:
            self.__lBlock = 'R-f'
            self.__rBlock = 'W-e'
        if self.__placement == 3:
            self.__lBlock = 'W-e'
            self.__rBlock = 'R-f'
        if self.__placement == 5:
            self.__lBlock = 'R-e'
            self.__rBlock = 'W-f'
        if self.__placement == 7:
            self.__lBlock = 'W-f'
            self.__rBlock = 'R-e'
        if self.__placement == 2:
            self.__tBlock = 'R-f'
            self.__bBlock = 'W-e'
        if self.__placement == 4:
            self.__tBlock = 'W-e'
            self.__bBlock = 'R-f'
        if self.__placement == 6:
            self.__tBlock = 'R-e'
            self.__bBlock = 'W-f'
        if self.__placement == 8:
            self.__tBlock = 'W-f'
            self.__bBlock = 'R-e'



    def printCard(self):
        print('\nCard Info: ')
        print('uid: ', self.__uid)
        print('placement: ', self.__placement)
        print('type: ', self.__type)
        if self.__type == 'horizontal':
            print('left: ', self.__lBlock)
            print('right: ', self.__rBlock)
        if self.__type == 'vertical':
            print('top: ',self.__tBlock)
            print('bottom: ',self.__bBlock)