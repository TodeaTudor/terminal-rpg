from Monsters.MonsterAblities import *
import random

basic_attack = MonsterAttackAbilities(10, 50)
ravenous_slash = MonsterAttackAbilities(25, 25)
greater_heal = MonsterHealingAbilities(50, 25)


class Imp:
    art = """  
         & &              @             
      @  &@#               &     &      
        @@@              # @     &      
       @&@@             #&&&@@(*#       
      & @ @    # ###### # # &@&&&@      
        @  @    ##### ##, &@@&@@        
           @    #    &&## &&&@&         
           @   #@@@@@@@@&&&&&&&         
            @@@@@ #@@&@  @@#@@          
           &&@###&@@@&&&@&# @@## #      
           @&@@@&@@@@@&&@@&@@@@@@&&&@   
             @#@@@@&@&@@@@@@@@@@@@@@    
             @ @@@@& &&&@@@@@@          
             @&  @@  &&&@@  &&          
              @ @@@@&  &@@&  &@     """

    def __init__(self):
        self.name = "Shaman Imp"
        self.attack = 5
        self.current_hp = 300
        self.max_hp = 300
        self.level = 1
        self.abilities = [basic_attack, ravenous_slash, greater_heal]
        self.ailments = []

    def cast_ability(self, char):
        is_frozen = False
        for ailment in self.ailments:
            if ailment.__class__.__name__ == "Freeze":
                is_frozen = True
        if not is_frozen:
            rand = random.randrange(99)
            if rand > 50:
                if rand < 75 or self.current_hp > self.max_hp - greater_heal.recovery:
                    char.current_hp -= ravenous_slash.attack
                else:
                    self.current_hp += greater_heal.recovery
            else:
                char.current_hp -= basic_attack.attack
