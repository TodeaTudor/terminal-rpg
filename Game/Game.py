import curses

combat_spacing = 33
screen_width = 150
screen_height = 50
combat_menu_width = 25
combat_pad_width = 75


def add_new_lines(nb_of_lines, screen):
    screen.addstr(nb_of_lines * '\n')


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, 209, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(7, 209, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(11, curses.COLOR_CYAN, curses.COLOR_BLACK)


def delete_line_from_x(pad, y, x):
    for i in range(x, screen_width):
        pad.delch(y, i)


def display_ticks(screen, curr, maximum, color):
    ticks = (curr/maximum) * 10
    screen.addstr(str(curr) + '/' + str(maximum) +
                  '[ ' + int(ticks) * 2 * '█' + (20 - 2*int(ticks)) * ' ' + ' ]',
                  curses.color_pair(color))


def max_length(line):
    maximum = 0
    for i in line:
        if len(i) > maximum:
            maximum = len(i)
    return maximum


def fit_in_screen(aux_l1, aux_l2):
    l1_line_length = max_length(aux_l1)
    l11 = ''
    for i in range(len(aux_l2) - len(aux_l1)):
        l11 += l1_line_length * ' ' + '\n'
    for i in aux_l1:
        l11 += i + (l1_line_length - len(i)) * ' ' + '\n'
    l1 = l11.split("\n")
    return l1


def display_hp_bars(screen, char):
    return display_ticks(screen, char.current_hp, char.max_hp, 1)


def display_enemy_hp_bar(screen, enemy):
    return display_ticks(screen, enemy.current_hp, enemy.max_hp, 5)


def display_resource_bar(screen, char):
    if char.__class__.__name__ == 'Warrior':
        return display_ticks(screen, char.current_resource, char.max_resource, 2)
    elif char.__class__.__name__ == 'Hunter':
        return display_ticks(screen, char.current_resource, char.max_resource, 3)
    elif char.__class__.__name__ == 'Sorcerer':
        return display_ticks(screen, char.current_resource, char.max_resource, 4)


def display_combat_screen(char, enemy):
    aux_l1 = char.art.split('\n')
    aux_l2 = enemy.art.split('\n')

    if len(aux_l1) < len(aux_l2):
        l1 = fit_in_screen(aux_l1, aux_l2)
        l2 = aux_l2
    elif len(aux_l2) < len(aux_l1):
        l2 = fit_in_screen(aux_l2, aux_l1)
        l1 = aux_l1
    elif len(aux_l1) == len(aux_l2):
        l1 = aux_l1
        l2 = aux_l2

    final = ''
    for i in range(min(len(l1), len(l2))):
        final += l1[i] + combat_spacing * ' ' + l2[i] + '\n'

    return final


def display_lower_hp(screen, char):
    len1 = max_length(char.art.split('\n')) - 30
    if len1 > 0:
        screen.addstr(int(len1 / 2) * ' ')
        display_hp_bars(screen, char)
        screen.addstr((int(len1 / 2) + combat_spacing) * ' ')
    else:
        display_hp_bars(screen, char)


def display_lower_enemy_hp(screen, char):
    len1 = max_length(char.art.split('\n')) - 30
    if len1 > 0:
        screen.addstr(int(len1 / 2) * ' ')
        display_enemy_hp_bar(screen, char)
    else:
        display_enemy_hp_bar(screen, char)


def display_lower_resource(screen, char):
    add_new_lines(2, screen)
    len1 = max_length(char.art.split('\n')) - 30
    if len1 > 0:
        screen.addstr(int(len1 / 2) * ' ')
        display_resource_bar(screen, char)
        screen.addstr((int(len1 / 2) + combat_spacing) * ' ')
    else:
        display_resource_bar(screen, char)


def display_info(screen, char, enemy):
    len1 = max_length(char.art.split('\n'))
    len2 = max_length(enemy.art.split('\n'))
    screen.addstr(2, len1, str(char.name))
    screen.addstr(3, len1, "Level:" + str(char.level))
    for i, ailment in enumerate(char.ailments):
        if ailment.__class__.__name__ == "Bleed":
            screen.addstr(5 + 2*i, len1, "Bleeding" + str(ailment.duration + 1) + " Turns", curses.color_pair(5))
        elif ailment.__class__.__name__ == "Freeze":
            screen.addstr(5 + 2*i, len1, "Frozen" + str(ailment.duration + 1) + " Turns", curses.color_pair(11))
    screen.addstr(2, len1 + len2 + combat_spacing, str(enemy.name))
    screen.addstr(3, len1 + len2 + combat_spacing, "Level:" + str(enemy.level))
    for i, ailment in enumerate(enemy.ailments):
        if ailment.__class__.__name__ == "Bleed":
            screen.addstr(5 + 2*i, len1 + len2 + combat_spacing, "Bleeding " + str(ailment.duration) + " Turns",
                          curses.color_pair(5))
        elif ailment.__class__.__name__ == "Freeze":
            screen.addstr(5 + 2*i, len1 + len2 + combat_spacing, "Frozen " + str(ailment.duration) + " Turns",
                          curses.color_pair(11))


def display_combat_scene(screen, char, enemy):
    art = display_combat_screen(char, enemy)
    screen.addstr(art)
    y, x = screen.getyx()
    display_info(screen, char, enemy)
    screen.addstr(y, x, "")
    add_new_lines(2, screen)
    display_lower_hp(screen, char)
    display_lower_enemy_hp(screen, enemy)
    display_lower_resource(screen, char)


def print_display_menu(screen, index, y, menu_type):
    menu_screen = curses.newwin(13, combat_menu_width, y, 5)
    menu_screen.border('|', '|', '-', '-', '+', '+', '+', '+')
    for current_index, entry in enumerate(menu_type):
        if index == current_index:
            menu_screen.addstr(2 + 2*current_index, 8, entry, curses.color_pair(6))
        else:
            menu_screen.addstr(2 + 2*current_index, 8, entry)
    screen.refresh()
    menu_screen.refresh()


def display_combat_menu(screen, y):
    menu_index = 0
    battle_menu = ['Attack', 'Inventory', 'Flee', 'Menu']
    print_display_menu(screen, menu_index, y, battle_menu)
    while 1:
        key = screen.getch()
        if key == curses.KEY_UP and menu_index > 0:
            menu_index -= 1
        elif key == curses.KEY_DOWN and menu_index < len(battle_menu) - 1:
            menu_index += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return menu_index
        print_display_menu(screen, menu_index, y, battle_menu)


def add_highlighted_attack(abilities_pad, char, entry):
    if entry.__class__.__name__ == "HealingAbilities":
        abilities_pad.addstr(entry.name, curses.color_pair(10))
    elif entry.__class__.__name__ == "AttackAbilities":
        if char.__class__.__name__ == 'Warrior':
            abilities_pad.addstr(entry.name, curses.color_pair(7))
        elif char.__class__.__name__ == 'Hunter':
            abilities_pad.addstr(entry.name, curses.color_pair(8))
        elif char.__class__.__name__ == 'Sorcerer':
            abilities_pad.addstr(entry.name, curses.color_pair(9))


def add_normal_attack(abilities_pad, char, entry):
    if entry.__class__.__name__ == "HealingAbilities":
        abilities_pad.addstr(entry.name, curses.color_pair(1))
    elif entry.__class__.__name__ == "AttackAbilities":
        if char.__class__.__name__ == 'Warrior':
            abilities_pad.addstr(entry.name, curses.color_pair(2))
        elif char.__class__.__name__ == 'Hunter':
            abilities_pad.addstr(entry.name, curses.color_pair(3))
        elif char.__class__.__name__ == 'Sorcerer':
            abilities_pad.addstr(entry.name, curses.color_pair(4))


def is_new_line_info(entry, index):
    new_index = index % (screen_width - combat_pad_width - 10)
    chars_until_eol = screen_width - combat_pad_width - 10 - new_index
    count = 0
    if len(entry) - index < chars_until_eol:
        return True
    while count < chars_until_eol and index < len(entry):
        if entry[index] == ' ':
            return True
        count += 1
        index += 1
    return False


def display_attack_ability(skill_screen, entry):
    skill_screen.addstr("Attack Ability")
    add_new_lines(2, skill_screen)
    skill_screen.addstr("Attack Damage: ")
    skill_screen.addstr(str(entry.attack), curses.color_pair(5))
    add_new_lines(2, skill_screen)
    skill_screen.addstr("Afflictions: ")
    add_new_lines(1, skill_screen)
    if entry.ailment_type.__class__.__name__ == "Bleed":
        skill_screen.addstr(
            str(entry.ailment_chance) + "% to cause bleeding for " + str(entry.ailment_type.base_duration) +
            " Turns", curses.color_pair(5))
    elif entry.ailment_type.__class__.__name__ == "Freeze":
        skill_screen.addstr(str(entry.ailment_chance) + "% to freeze for " + str(entry.ailment_type.base_duration) +
                            " Turns", curses.color_pair(11))
    if entry.base_cooldown > 0:
        add_new_lines(2, skill_screen)
        skill_screen.addstr("Cooldown: " + str(entry.base_cooldown) + " Turns")


def display_healing_ability(skill_screen, entry):
    skill_screen.addstr("Healing Ability")
    add_new_lines(2, skill_screen)
    skill_screen.addstr("Recovery Rate: ")
    skill_screen.addstr(str(entry.recovery), curses.color_pair(1))


def display_attack_info(screen, entry, y, char):
    skill_screen = curses.newwin(screen_height - y + 1, screen_width - combat_pad_width - 10, y, combat_pad_width + 9)
    skill_screen.addstr(entry.name)
    add_new_lines(2, skill_screen)
    for index, character in enumerate(entry.description):
        if character == ' ':
            if not is_new_line_info(entry.description, index + 1) \
                    and len(entry.description) > screen_width - combat_pad_width - 10:
                add_new_lines(1, skill_screen)
                continue
        skill_screen.addstr(character)
    add_new_lines(2, skill_screen)
    if entry.__class__.__name__ == "AttackAbilities":
        display_attack_ability(skill_screen, entry)
    elif entry.__class__.__name__ == "HealingAbilities":
        display_healing_ability(skill_screen, entry)
    add_new_lines(2, skill_screen)
    skill_screen.addstr("Resource Cost: ")
    if char.__class__.__name__ == 'Warrior':
        skill_screen.addstr(str(entry.cost) + " Fury", curses.color_pair(2))
    elif char.__class__.__name__ == 'Hunter':
        skill_screen.addstr(str(entry.cost) + " Stamina", curses.color_pair(3))
    elif char.__class__.__name__ == 'Sorcerer':
        skill_screen.addstr(str(entry.cost) + " Mana", curses.color_pair(4))
    skill_screen.refresh()
    screen.refresh()


def print_attacks_menu(abilities_pad, abilities_pad_pos, y, char, screen):
    abilities_pad.clear()
    abilities_screen = curses.newwin(16, combat_pad_width - combat_menu_width, y - 1, combat_menu_width + 6)
    abilities_screen.border('|', '|', '-', '-', '+', '+', '+', '+')
    abilities_screen.refresh()
    for current_index, entry in enumerate(char.attacks):
        if abilities_pad_pos == current_index:
            add_highlighted_attack(abilities_pad, char, entry)
            display_attack_info(screen, entry, y, char)
        else:
            add_normal_attack(abilities_pad, char, entry)
        if entry.remaining_cooldown != 0:
            abilities_pad.addstr(' ' + str(entry.remaining_cooldown) + '\n', curses.color_pair(5))
        else:
            add_new_lines(1, abilities_pad)
    screen.addstr(screen_height - 4, 30, "ESC-Back")
    abilities_pad.refresh(abilities_pad_pos, 0, y, combat_menu_width + 10, y + 13, combat_pad_width)


def display_attack_pad(screen, y, char):
    abilities_pad = curses.newpad(len(char.attacks) + 1, combat_pad_width)
    abilities_pad_pos = 0
    print_attacks_menu(abilities_pad, abilities_pad_pos, y, char, screen)

    while 1:
        key = screen.getch()
        if key == curses.KEY_UP and abilities_pad_pos > 0:
            abilities_pad_pos -= 1
        elif key == curses.KEY_DOWN and abilities_pad_pos < len(char.attacks) - 1:
            abilities_pad_pos += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if char.attacks[abilities_pad_pos].remaining_cooldown == 0:
                return abilities_pad_pos
        elif key == 27:
            return None
        print_attacks_menu(abilities_pad, abilities_pad_pos, y, char, screen)


def display_attack_menu(screen, y, char, enemy):
    pressed_index = display_attack_pad(screen, y, char)
    if pressed_index is not None:
        char.cast_ability(enemy, char.attacks[pressed_index])
        enemy.cast_ability(char)


def display_item_info(entry, y):
    item_screen = curses.newwin(screen_height - y + 1, screen_width - combat_pad_width - 10, y, combat_pad_width + 9)
    if entry.__class__.__name__ == "HealingPotion":
        item_screen.addstr("Heals you for " + str(entry.restored_hp) + " HP", curses.color_pair(1))
    else:
        item_screen.addstr("Heals you for " + str(entry.restored_resource) + " Fury", curses.color_pair(2))
    item_screen.refresh()


def print_items_menu(items_pad, items_pad_pos, y, char, screen):
    items_pad.clear()
    abilities_screen = curses.newwin(16, combat_pad_width - combat_menu_width, y - 1, combat_menu_width + 6)
    abilities_screen.border('|', '|', '-', '-', '+', '+', '+', '+')
    abilities_screen.refresh()
    for current_index, (entry, quantity) in enumerate(char.inventory.items()):
        if items_pad_pos == current_index:
            items_pad.addstr(entry.name + " " + str(quantity), curses.color_pair(6))
            display_item_info(entry, y)
        else:
            items_pad.addstr(entry.name + " " + str(quantity), curses.color_pair(3))
        add_new_lines(1, items_pad)
    screen.addstr(screen_height - 4, 30, "ESC-Back")
    items_pad.refresh(items_pad_pos, 0, y, combat_menu_width + 10, y + 13, combat_pad_width)


def display_item_pad(screen, y, char):
    items_pad = curses.newpad(len(char.inventory) + 1, combat_pad_width)
    items_pad_pos = 0
    print_items_menu(items_pad, items_pad_pos, y, char, screen)

    while 1:
        key = screen.getch()
        if key == curses.KEY_UP and items_pad_pos > 0:
            items_pad_pos -= 1
        elif key == curses.KEY_DOWN and items_pad_pos < len(char.inventory) - 1:
            items_pad_pos += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return items_pad_pos
        elif key == 27:
            return None
        print_items_menu(items_pad, items_pad_pos, y, char, screen)


def display_item_menu(screen, y, char):
    pressed = display_item_pad(screen, y, char)
    char.consume_item(pressed)


def display_intro_screen(screen):
    while 1:
        screen.addstr((screen_height // 2) - 10, screen_width // 4,
                      '''
                      While traversing the Dark Forest you meet with a creature most foul. 
                      An Imp with a wooden rod from which wicked charms hang stops you dead in your tracks. 
                      It starts muttering curses in a language unknown to you. 
                      It leaves you but with one choice: to bathe the ground beneath your feet with its blood.
                      
                      Press Enter to continue.
                      ''')
        key = screen.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            break


def display_outro_scene(screen):
    while 1:
        screen.addstr((screen_height // 2) - 10, screen_width // 4,
                      '''
                      As the dust settles and the creature draws its final breath, you feel the weight of your sword in your hands. 
                      You stop for a moment to catch your breath, staring at the corpse of your foe.
                      "One less corrupted soul in this land", you mutter under your breath. 
                      One less corrupted soul, indeed. 
                      But who knows how many more will succumb to your blade until your deed is done.
                      Alas, provided you will not succumb to theirs before that.
                      
                      Press ESC to close the game.
                      ''')
        key = screen.getch()
        if key == 27:
            break


def display_scene_1(screen, char, enemy):
    while 1:
        display_combat_scene(screen, char, enemy)
        add_new_lines(1, screen)
        screen.addstr(screen_width * '=')
        add_new_lines(1, screen)
        y, x = screen.getyx()
        pressed = display_combat_menu(screen, y)
        screen.refresh()
        if pressed == 0:
            display_attack_menu(screen, y, char, enemy)
        if pressed == 1:
            display_item_menu(screen, y, char)
        if pressed == 2:
            screen.clear()
            screen.addstr((screen_height // 2) - 10, screen_width // 4,
                          "You fled like a coward. Press ESC to close the game.")
            key = screen.getch()
            if key == 27:
                break
        if enemy.current_hp == 0:
            screen.clear()
            display_outro_scene(screen)
            break
        screen.clear()
