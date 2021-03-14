class Consumable:
    def __init__(self, name):
        self.name = name

    def consume(self, char):
        pass


class HealingPotion(Consumable):
    def __init__(self, name, restored_hp):
        super().__init__(name)
        self.restored_hp = restored_hp

    def consume(self, char):
        if char.current_hp < char.max_hp - self.restored_hp:
            char.current_hp += self.restored_hp
        else:
            char.current_hp = char.max_hp


class ResourcePotion(Consumable):
    def __init__(self, name, restored_resource):
        super().__init__(name)
        self.restored_resource = restored_resource

    def consume(self, char):
        if char.current_resource < char.max_resource - self.restored_resource:
            char.current_resource += self.restored_resource
        else:
            char.current_resource = char.max_resource


small_hp_pot = HealingPotion("Small HP Potion", 50)
small_fury_pot = ResourcePotion("Small Fury Potion", 20)