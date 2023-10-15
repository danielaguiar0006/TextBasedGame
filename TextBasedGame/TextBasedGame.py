# Daniel Aguiar
# 10/13/2023
# Mini Text-Based Game for IT-140 Class

# Player class representing the main character in the game.
class Player():
    def __init__(self):
        # Initial attributes for the player.
        self.location = 'Entrance Hall'  # Starting location
        self.max_health = 100  # Max health
        self.health = self.max_health  # Initial health
        self.damage = 50  # Base damage
        self.inventory = []  # Player's items
        self.is_alive = True  # Player's status

    # Method to move the player to a new location.
    def move(self, direction, rooms):
        if direction in rooms[self.location]:
            self.location = rooms[self.location][direction]
            print('You are now in', self.location)
        else:
            print('You can\'t go that way! Please try again.')

    # Method to pick up items.
    def pick_up(self, item_name, room_items, is_action_turn_completed):
        item_found = False
        for item in room_items[self.location]:
            if item.name.title() == item_name:
                item_found = True
                self.inventory.append(item)
                room_items[self.location].remove(item)
                print('You picked up', item.name)

                # TODO? A better way to do this is to have a player equip method
                # to edit health and attack attributes with items like chestplate or sword
                if item.effect == 'increase health':
                    self.max_health += item.value
                    self.health += item.value
                    print(f'Max health increased by {item.value}! (Max health now: {self.max_health})')
                elif item.effect == 'increase damage':
                    self.damage += item.value
                    print(f'Attack damage increased by {item.value}! (Attack dammage now: {self.damage})')

                # Player's turn completed
                is_action_turn_completed = True
                break

        if not item_found:
            print(f'Error... no item named "{item_name}" in room.')
            # Player's turn not completed succesfully
            is_action_turn_completed = False

        return is_action_turn_completed

    # Method to attack mobs.
    def attack(self, mob_name, room_mobs, is_action_turn_completed):
        target_mob = None
        for mob in room_mobs[self.location]:
            if mob.name.title() == mob_name and mob.is_attackable:
                target_mob = mob
                break

        if target_mob:
            damage_done = self.damage
            # TODO could add logic to add additional effects like random critial effects or poision here

            target_mob.health -= damage_done
            is_action_turn_completed = True
            print(f'You did {damage_done} damage to {target_mob.name}!')
        else:
            is_action_turn_completed = False
            print(f"There's no {mob_name} here to attack.")

        return is_action_turn_completed

    # Method to use items
    def use_item(self, item_name):
        # Look for the item in the inventory.
        item_to_use = next((item for item in self.inventory if item.name.title() == item_name), None)

        if not item_to_use:
            print(f"You don't have a {item_name} in your inventory.")
            return

        # If the item is consumable, apply its effect.
        if item_to_use.consumable:
            if item_to_use.effect == "heal":
                # Limiting healing effect to not go past players max health
                if self.health + item_to_use.value > self.max_health:
                    self.health = self.max_health
                    print(f"You used {item_name} and restored {self.max_health - self.health} health points!")
                else:
                    self.health += item_to_use.value
                    print(f"You used {item_name} and restored {item_to_use.value} health points!")
            # Add more effects as needed here using elif statements.

            # Remove the item from the inventory.
            self.inventory.remove(item_to_use)
        else:
            print(f"{item_name} is not consumable.")

    def display_item_info(self, item_name):  # TODO maybe add to show player info too
        # Look for the item in the inventory.
        item_for_info = next((item for item in self.inventory if item.name.title() == item_name), None)

        # Display info
        if item_for_info:
            # If item effects attributes:
            if item_for_info.effect and item_for_info.value:
                # Determine sign for info
                sign = '+' if item_for_info.value >= 0 else '-'
                print(f"{item_for_info.description} ({item_for_info.effect}: {sign}{item_for_info.value})")
            else:
                print(f"{item_for_info.description}")
        else:
            print(f"You don't have a {item_name} in your inventory.")

    # Check the health of the player.
    def check_health(self):
        if self.health <= 0:
            self.is_alive = False
            print("Game Over you died!")


# Mob class representing the enemies in the game.
class Mob():
    def __init__(self, name, health, damage, is_attackable=True):
        # Initial attributes for the mob.
        self.name = name
        self.health = health
        self.damage = damage
        self.is_attackable = is_attackable
        self.is_alive = True

    # Method for mob to attack the player.
    def attack_player(self, player):
        if self.is_attackable:
            print(f"{self.name} attacks you for {self.damage} damage!")
            player.health -= self.damage
            player.check_health()

    # Method to check the mob's health and remove it if it's dead.
    def check_health(self, room_mobs, location, room_items):
        if self.health <= 0:
            self.is_alive = False
            print(f'{self.name} has been defeated!')
            room_mobs[location].remove(self)

            # If the mob is the dragon, add the dragon's heart to the room.
            if self.name == 'Ancient Dragon':
                dragon_heart_item = Item('Ancient Dragon\'s Heart', 'The very essence of the ancient dragon, pulsating '
                                                                    'with energy.', effect='ends game')
                room_items[location].append(dragon_heart_item)
                print(f"{self.name} dropped {dragon_heart_item.name}!")


# Item class representing items that can be picked up in the game.
class Item():
    def __init__(self, name, description, consumable=False, effect=None, value=None):
        # Initial attributes for items.
        self.name = name
        self.description = description
        self.consumable = consumable
        self.effect = effect  # This can be a string such as "heal", "boost", etc.
        self.value = value  # Represents the magnitude of the effect.


# Setup function to initialize game settings and world before main game loop.
def setup():
    # Map of all rooms
    rooms_map = {'Entrance Hall': {'East': 'The Majestic Dining Room'},
                 'The Majestic Dining Room': {'North': 'The Desolate Kitchen', 'East': 'The Cursed Dungeon',
                                              'South': 'The Abandoned Bedroom', 'West': 'Entrance Hall'},
                 'The Desolate Kitchen': {'East': 'The Haunted Chamber', 'South': 'The Majestic Dining Room'},
                 'The Haunted Chamber': {'West': 'The Desolate Kitchen'},
                 'The Cursed Dungeon': {'North': 'The Dragon\'s Lair', 'West': 'The Majestic Dining Room'},
                 'The Dragon\'s Lair': {'South': 'The Cursed Dungeon'},
                 'The Abandoned Bedroom': {'North': 'The Majestic Dining Room', 'East': 'The Forgotten Library'},
                 'The Forgotten Library': {'East': 'The Abandoned Bedroom'}
                 }

    # Create items
    scroll_item = Item('Lost Scroll', 'A timeworn scroll, its edges frayed with age. Unrolling it reveals cryptic \n'
                                      'runes and a message: "Beware, adventurer, for the depths of the lair hold \n'
                                      'perils beyond imagination. Tread with caution."')
    health_potion_item_1 = Item('Elixir of Vitality',
                                'A shimmering red potion that restores vitality and mends wounds.',
                                consumable=True, effect='heal', value=100)
    health_potion_item_2 = Item('Elixir of Vitality', 'A rejuvenating concoction that instantly heals minor injuries.',
                                consumable=True, effect='heal', value=100)
    health_potion_item_3 = Item('Elixir of Vitality', 'A deep red potion, promising swift recovery from injuries.',
                                consumable=True, effect='heal', value=100)
    health_potion_item_4 = Item('Elixir of Vitality', 'A deep red potion, promising swift recovery from injuries.',
                                consumable=True, effect='heal', value=100)
    enchanted_armour_item = Item('Enchanted Chestplate',
                                 'A gleaming chestplate imbued with protective spells. It lessens the impact of enemy '
                                 'blows.', effect='increase health', value=50)
    enchanted_amulet_item = Item('Enchanted Amulet', 'A radiant amulet set with a gem that pulses with a soft light. '
                                                     'Its wearer feels an unmistakable aura of protection enveloping '
                                                     'them.', effect='increase health', value=25)
    enchanted_ring_item = Item('Enchanted Ring', 'A delicately crafted ring, adorned with intricate runes that glow '
                                                 'faintly. When worn, one can feel a surge of strength coursing '
                                                 'through their veins.', effect='increase damage', value=25)
    sword_item = Item('The Dragon Slayer Sword',
                      'A legendary blade, forged in dragonfire and imbued with the power to vanquish the mightiest of '
                      'dragons.', effect='increase damage', value=100)

    # Create mobs
    undead_skeleton_soldier_1 = Mob('Undead Skeleton Soldier', health=100, damage=30)
    undead_skeleton_soldier_2 = Mob('Undead Skeleton Soldier', health=100, damage=30)
    undead_skeleton_soldier_3 = Mob('Undead Skeleton Soldier', health=100, damage=30)
    zombie_1 = Mob('Wretched Zombie', health=75, damage=25)
    zombie_2 = Mob('Wretched Zombie', health=75, damage=25)
    zombie_3 = Mob('Wretched Zombie', health=75, damage=25)
    hell_hound_1 = Mob('Hell Hound', health=75, damage=20)
    hell_hound_2 = Mob('Hell Hound', health=75, damage=20)
    hell_hound_3 = Mob('Hell Hound', health=75, damage=20)
    dragon = Mob('Ancient Dragon', health=500, damage=60)

    # Map items to rooms # TODO NEED TO REARRANGE ITEM AND MOB MAP (working on it...)
    room_items = {'Entrance Hall': [scroll_item, health_potion_item_1],
                  'The Majestic Dining Room': [],
                  'The Desolate Kitchen': [health_potion_item_2],
                  'The Haunted Chamber': [enchanted_armour_item],
                  'The Cursed Dungeon': [health_potion_item_3, sword_item],
                  'The Dragon\'s Lair': [],
                  'The Abandoned Bedroom': [health_potion_item_4],
                  'The Forgotten Library': [enchanted_amulet_item, enchanted_ring_item]
                  }

    # Map mobs to rooms
    room_mobs = {'Entrance Hall': [],
                 'The Majestic Dining Room': [zombie_1],
                 'The Desolate Kitchen': [undead_skeleton_soldier_1],
                 'The Haunted Chamber': [undead_skeleton_soldier_2, undead_skeleton_soldier_3],
                 'The Cursed Dungeon': [hell_hound_1, hell_hound_2, hell_hound_3],
                 'The Dragon\'s Lair': [dragon],
                 'The Abandoned Bedroom': [zombie_2, zombie_3],
                 'The Forgotten Library': []
                 }
    return rooms_map, room_items, room_mobs


# Main function that drives the game.
def main():
    rooms_map, room_items, room_mobs = setup()
    player = Player()
    game_ending_condition = False

    show_instructions()

    # main game loop
    while player.is_alive and not game_ending_condition:
        display_hud(player, rooms_map, room_mobs, room_items)

        is_action_turn_completed = None
        action_type, command = handle_input()

        print('\n*************************************')

        # Players turn         # ? Match case could be used instead...
        if action_type == 'go' or action_type == 'move':
            is_action_turn_completed = False
            player.move(command, rooms_map)
        elif action_type == 'get' or action_type == 'pickup':
            # Will return true if an item is actually picked up
            is_action_turn_completed = player.pick_up(command, room_items, is_action_turn_completed)
        elif action_type == 'hit' or action_type == 'attack':
            # Will return true if valid enemy is attacked
            is_action_turn_completed = player.attack(command, room_mobs, is_action_turn_completed)  # TODO same as above
        elif action_type == 'use':
            is_action_turn_completed = False
            player.use_item(command)
        elif action_type == 'info' or action_type == 'display':
            is_action_turn_completed = False
            player.display_item_info(command)
        else:
            is_action_turn_completed = False
            print('Invalid action')

        # Enemy turn
        if is_action_turn_completed:
            for mob in room_mobs[player.location][:]:  # Copy the list for iteration
                mob.check_health(room_mobs, player.location, room_items)  # Passing room_items to check_health
                if mob.is_alive:  # Only alive mobs will attack
                    mob.attack_player(player)

        # Checking game ending condition
        for item in player.inventory:  # TODO ADD CONGRATS SCREEN FOR SLAYING DRAGON
            if item.effect == 'ends game':
                game_ending_condition = True
            else:
                continue

        print('*************************************')

        if game_ending_condition:
            display_congrats_screen()


# Function to process player's input.
def handle_input():
    command = input('Enter your move: ').split()
    action_type = command[0].lower()
    command = ' '.join(command[1:]).title()

    return action_type, command


# Display game instructions at the start.
def show_instructions():  # TODO Display alternative input commands
    # print a main menu and the commands
    print("The Depths")
    print("Adventure into the depths and slay the dragon.")
    print("Move commands: go South, go North, go East, go West, exit")
    print("Add to Inventory: get 'item name'")
    print("Use item in inventory: use 'item name'")
    print("Display item info: info 'item name' (also must be in inventory)")
    print("Attack enemy: hit 'enemy name'\n")


# Display the game's heads-up display to give player context.
def display_hud(player, rooms_map, room_mobs, room_items):
    print(f'\nCurrent Room: {player.location}')

    # Display monsters in the room.
    if room_mobs[player.location]:
        monsters = [f"{mob.name} (Health: {mob.health})" for mob in room_mobs[player.location]]
        print('Monsters in room:', ', '.join(monsters))
    else:
        print('No monsters in this room.')

    # Display items in the room.
    if room_items[player.location]:
        items = [item.name for item in room_items[player.location]]
        print('Items in room:', ', '.join(items))
    else:
        print('No items in this room.')

    # Display player's health.
    print(f'\nPlayer Health: {player.health}')

    # Display player's inventory.
    inventory_items = [item.name for item in player.inventory]
    if inventory_items:
        print('Inventory:', ', '.join(inventory_items))
    else:
        print('Inventory: Empty')

    # Display available directions.
    print(f"Available directions: {', '.join(rooms_map[player.location].keys())}")

    print('-------------------------------------')


def display_congrats_screen():
    print("\n\n")
    print("*****************************************")
    print("*                                       *")
    print("*       CONGRATULATIONS, HERO!          *")
    print("*                                       *")
    print("*   You have slain the Ancient Dragon   *")
    print("*   and saved the realm from its terror! *")
    print("*                                       *")
    print("*****************************************")
    print("\n\n")


# Start the game.
main()
