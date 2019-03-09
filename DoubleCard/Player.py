class Player:
    def __init__(self, name, number, cards):
        # rotation number
        self.__name = name
        self.__number = number
        self.__objective = ''
        self.__cards = cards

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