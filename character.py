class Character():
    def __init__(self, char_name, char_description):
        self.name = char_name
        self.description = char_description
        self.conversation = None
        self.block = 0
        self.complex = False
        self.str = 0
        self.dex = 0
    # Describe this character
    def describe(self):
        print( "You spot a " + self.name)
        print( self.description )
    # Set what this character will say when talked to
    def set_conversation(self, conversation):
        self.conversation = conversation
    # Talk to this character
    def talk(self):
        if self.conversation is not None:
            print("[" + self.name + "]: " + self.conversation)
        else:
            print(self.name + " doesn't want to talk to you")
    # Fight with this character
    def fight(self, combat_item):
        print(self.name + " doesn't want to fight with you")
        return True

class Enemy(Character):
    enemies_to_defeat = 0
    def __init__(self, char_name, char_description):
        super().__init__(char_name, char_description)
        self.weakness = None
        self.poison = 0
        self.frostbite = 0
        Enemy.enemies_to_defeat += 1
    def fight(self, combat_item, strength):
        for i in combat_item['damage']:
            self.take_damage(i + strength)
        if self.health>0:
            return False
        else:
            print(f'{self.name} is dead')
            return True


    def get_weakness(self):
        return self.weakness
    def set_weakness(self, weakness):
        self.weakness=weakness
    def steal(self):
        print('You stole from '+self.name)
    def set_health(self, health):
        self.health = health
    def take_damage(self, damage):
        if damage>0:
            self.block -= int(damage*(1+self.frostbite))
            if self.block<0:
                self.health += self.block
                self.block=0
    def set_action(self, damage, block):
        self.action = {
            'Attack':damage,
            'Block':block
            }
    def set_actions(self, action1, action2):
        self.complex = True
        self.actions = [{'Attack':action1[0], 'Block':action1[1]},{'Attack':action2[0],'Block':action2[1]}]
    def set_actionss(self, action1, action2, action3, action4):
        self.complex = True
        self.actions = [{'Attack':action1[0], 'Block':action1[1]},{'Attack':action2[0],'Block':action2[1]},{'Attack':action3[0], 'Block':action3[1]},{'Attack':action4[0],'Block':action4[1]}]
    def set_block(self, block):
        self.block += block
    def reset_block(self):
        self.block = 0

class Friend(Character):
    def __init__(self, char_name, char_description):
        super().__init__(char_name, char_description)
        self.feeling = None
    def pat(self):
        print(self.name + " pats you back!")

