class Item():
    def __init__(self, item_name):
        self.name = item_name
        self.loss = 0
        self.poison = 0
        self.money = 0
    def get_name(self):
        return self.name
    def set_name(self, item_name):
        self.name = item_name
    def get_description(self):
        return self.description
    def set_description(self, item_description):
        self.description = item_description
    def describe(self):
        print ("You found a [" + self.name + "] - " + self.description)

class Card(Item):
    def __init__(self, item_name):
        super().__init__(item_name)
        self.exhaust = False
        self.action={
'damage':[],
'block':[],
'draw':[]
            }
    def create(self, card_function):
        for i in card_function:
            if i[0] == 'Attack':
                self.action['damage'].append(i[1])
            elif i[0] == 'Block':
                self.action['block'].append(i[1])
            elif i[0] == 'Draw':
                self.action['draw'].append(i[1])

    def set_cost(self, cost):
        self.cost = cost

    def set_hp_loss(self, loss):
        self.loss = loss
    def set_poison(self, poison):
        self.poison = poison

