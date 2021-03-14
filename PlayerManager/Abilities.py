class Ailments:
    def __init__(self, duration):
        self.duration = duration
        self.base_duration = duration


class Bleed(Ailments):
    def __init__(self, duration, base_damage):
        super().__init__(duration)
        self.damage = base_damage
        self.base_damage = base_damage


class Freeze(Ailments):
    def __init__(self, duration):
        super().__init__(duration)


class Abilities:
    def __init__(self, name, cost, description, cooldown):
        self.name = name
        self.cost = cost
        self.description = description
        self.base_cooldown = cooldown
        self.remaining_cooldown = 0


class AttackAbilities(Abilities):
    def __init__(self, attack, cost, description=None, name=None, ailment_chance=0, ailment_type=None, cooldown=0):
        super().__init__(name, cost, description, cooldown)
        self.attack = attack
        self.ailment_chance = ailment_chance
        self.ailment_type = ailment_type


class HealingAbilities(Abilities):
    def __init__(self, recovery, cost, description=None, name=None, cooldown=0, ailment_removal=None):
        super().__init__(name, cost, description, cooldown)
        self.recovery = recovery
        self.ailment_removal = ailment_removal


bleeding = Bleed(3, 5)
stun = Freeze(2)


