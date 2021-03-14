from PlayerManager.Abilities import *
from PlayerManager.Item import *
import random
from copy import deepcopy


def cast_attack_ability(enemy, ability):
    if enemy.ailments is not None:
        for ailment in enemy.ailments:
            if ailment.__class__.__name__ == "Bleed":
                if enemy.current_hp - ailment.damage > 0:
                    enemy.current_hp -= ailment.damage
    if enemy.current_hp - ability.attack > 0:
        enemy.current_hp -= ability.attack
    else:
        enemy.current_hp = 0
        return 1
    if ability.ailment_type is not None:
        if random.randrange(99) < ability.ailment_chance:
            present = False
            for ailment in enemy.ailments:
                if ailment.__class__.__name__ == ability.ailment_type.__class__.__name__:
                    ailment.duration += ability.ailment_type.duration
                    present = True
            if not present:
                enemy.ailments.append(deepcopy(ability.ailment_type))


def increase_ailment_duration(ability, ailments):
    for ailment in ailments:
        if ailment == ability.ailment_type:
            ailment.duration += ability.ailment_type.duration


class Player:
    def __init__(self, name, hp, basic_attack_damage,
                 critical_strike_damage_multiplier,
                 critical_strike_chance, resource):
        self.name = name
        self.base_hp = hp
        self.max_hp = hp
        self.basic_attack_damage = basic_attack_damage
        self.critical_strike_chance = critical_strike_chance
        self.critical_strike_damage_multiplier = critical_strike_damage_multiplier
        self.body_armour = None
        self.weapon = None
        self.boots = None
        self.belt = None
        self.helmet = None
        self.trinket = None
        self.inventory = {small_hp_pot: 10, small_fury_pot: 5}
        self.level = 1
        self.exp = 0
        self.attacks = []
        self.current_hp = hp
        self.max_resource = resource
        self.current_resource = resource
        self.base_resource = resource
        self.ailments = []

    def is_frozen(self):
        for ailment in self.ailments:
            if ailment.__class__.__name__ == "Freeze":
                ailment.duration -= 1
                if ailment.duration == 0:
                    self.ailments.remove(ailment)
                return True
        return False

    def cast_healing_ability(self, ability):
        if self.current_hp + ability.recovery > self.max_hp:
            self.current_hp = self.max_hp
        else:
            self.current_hp += ability.recovery

    def cast_ability(self, enemy, ability):
        for ailment in self.ailments:
            ailment.duration -= 1
            if ailment.duration == 0:
                self.ailments.remove(ailment)
        for ailment in enemy.ailments:
            ailment.duration -= 1
            if ailment.duration == 0:
                enemy.ailments.remove(ailment)
        if not self.is_frozen():
            if ability.__class__.__name__ == "AttackAbilities":
                cast_attack_ability(enemy, ability)
            elif ability.__class__.__name__ == "HealingAbilities":
                self.cast_healing_ability(ability)
            self.current_resource -= ability.cost
            ability.remaining_cooldown = ability.base_cooldown
        for entry in self.attacks:
            if entry.remaining_cooldown != 0 and entry != ability:
                entry.remaining_cooldown -= 1

    def consume_item(self, item_index):
        for index, (item, quantity) in enumerate(self.inventory.items()):
            if item_index == index:
                item.consume(self)
                self.inventory[item] -= 1
                if quantity == 1:
                    self.inventory.pop(item)


class Sorcerer(Player):

    def __init__(self, name):
        super().__init__(name, 550, 50, 200, 60, 750)


class Warrior(Player):

    art = """
           &* &                                  
          @///,,&                                 
          @///,*&                                 
           @///*.@&&  #   &&& #                   
           @///*.@%%%%%%%%&%%%%@& @/              
           @///*.@@&%%%&&&&%%###%##&@             
            & //* @@&&&&@&%#//%#&@@/              
            & //*.@/#/&&..@@,,&@@                 
          #&& ///,&&% &/*,,,***###                
            &@@&&@@@%%%%//@@/##//#@/              
           /&@&#,/.@@@@@,,,,,/###..@              
            /%#**@@@@////////@@@                  
              %@&/@&&%&&&&&%@                     
                 %%%%%&&&&&%%&#                   
               #@@@&@@@&  @@@@@&@                 
               #@#@@@      @#@@&#@             """

    def init_attacks(self):
        attacks = []
        basic_attack = AttackAbilities(self.basic_attack_damage * 1.5,
                                       0,
                                       "A basic attack. Anyone could perform it.",
                                       "Basic Attack",
                                       30,
                                       bleeding,
                                       0)

        gather_strength = HealingAbilities(20,
                                           20,
                                           "You take a moment of respite and feel the strength surging back into your body.",
                                           "Gather Strength",
                                           2,
                                           True)

        stun_attack = AttackAbilities(self.basic_attack_damage * 3,
                                      20,
                                      "Deal a deafening blow to your enemy.",
                                      "Stun Attack",
                                      100,
                                      stun,
                                      2)

        attacks.append(basic_attack)
        attacks.append(gather_strength)
        attacks.append(stun_attack)
        return attacks

    def __init__(self, name):
        super().__init__(name, 750, 15, 100, 30, 500)
        self.attacks = self.init_attacks()


class Hunter(Player):
    def __init__(self, name):
        super().__init__(name, 500, 100, 300, 50, 650)
