class Card:

    #ctor
    def __init__(self):
        #rotation number
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
            self.__lBlock = 'Rf'
            self.__rBlock = 'We'
        if self.__placement == 3:
            self.__lBlock = 'We'
            self.__rBlock = 'Rf'
        if self.__placement == 5:
            self.__lBlock = 'Re'
            self.__rBlock = 'Wf'
        if self.__placement == 7:
            self.__lBlock = 'Wf'
            self.__rBlock = 'Re'
        if self.__placement == 2:
            self.__tBlock = 'Rf'
            self.__bBlock = 'We'
        if self.__placement == 4:
            self.__tBlock = 'We'
            self.__bBlock = 'Rf'
        if self.__placement == 6:
            self.__tBlock = 'Re'
            self.__bBlock = 'Wf'
        if self.__placement == 8:
            self.__tBlock = 'Wf'
            self.__bBlock = 'Re'



    def printCard(self):
        print(self.__placement)
        print(self.__type)
        if self.__type == 'horizontal':
            print(self.__lBlock)
            print(self.__rBlock)
        if self.__type == 'vertical':
            print(self.__tBlock)
            print(self.__bBlock)




card = Card()
card.setPlacement(3)
card.printCard()