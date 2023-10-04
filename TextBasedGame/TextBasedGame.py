# Daniel Aguiar
class Player():
    def __init__(self):
        self.location = 'Entrance Hall'
        self.health = 100  # Max health
        self.damage = 50
        self.inventory = []
        self.is_alive = True

    def move(self, direction, rooms):
        if direction in rooms[self.location]:
            self.location = rooms[self.location][direction]
            print('You are now in', self.location)
        else:
            print('Invalid dirrection')

    def pick_up(self, item, room_items):
        if item.name in room_items[self.location]:
            self.inventory.append(item)

    def attack(self, mob, room_mobs):
        if mob in room_mobs[self.location] and mob.is_attackable:
            damage_done = self.damage  # Default damage
            for item in self.inventory:
                if item.name == 'Dragon Slayer Sword':
                    damage_done = 100
                    break
            mob.health -= damage_done
            print(f'You did {damage_done} damage!')

    # def use_item(self, item_name):

    def check_health(self):
        if self.health <= 0:
            self.is_alive = False
            print("Game Over you died!")


class Mob():
    def __init__(self, name, health, damage, is_attackable=True):
        self.name = name
        self.health = health
        self.damage = damage
        self.is_attackable = is_attackable


class Item():
    def __init__(self, name, description, consumable=False, effect=None):
        self.name = name
        self.description = description
        self.consumable = consumable
        self.effect = effect  # This can be a function or any other effect mechanism


def main():
    player = Player()

    # Items in the game
    torch_item = Item('Torch', 'no description')
    health_potion = Item('Elixir of Vitality', 'health potion', consumable=True)  # ! NEEDS TO AFFECTS PLAYERS HEALTH
    enchanted_armour = Item('Enchanted Chestplate', 'Provides more protection against attacks')
    sword_item = Item('The Dragon Slayer Sword', 'Big sword which increases attack power substantially')
    key_item = Item('Rusty Key', 'Who knows what it unlocks, but surely it\'s for something special...',
                    consumable=True)

    # Mobs in the game
    undead_soldier_1 = Mob('Undead Soldier', health=100, damage=20)
    undead_soldier_2 = Mob('Undead Soldier', health=100, damage=20)
    hell_hound_1 = Mob('Hell Hound', health=75, damage=15)
    hell_hound_2 = Mob('Hell Hound', health=75, damage=15)
    hell_hound_3 = Mob('Hell Hound', health=75, damage=15)

    # Map of all of our rooms in the game and their relative direction to each other
    rooms = {'Entrance Hall': {'East': 'The Majestic Dining Room'},
             'The Majestic Dining Room': {'North': 'The Desolate Kitchen', 'East': 'The Cursed Dungeon',
                                          'South': 'The Abandoned Bedroom', 'West': 'Entrance Hall'},
             'The Desolate Kitchen': {'East': 'The Haunted Chamber', 'South': 'The Majestic Dining Room'},
             'The Haunted Chamber': {'West': 'The Desolate Kitchen'},
             'The Cursed Dungeon': {'North': 'The Dragon\'s Lair', 'West': 'The Majestic Dining Room'},
             'The Dragon\'s Lair': {'South': 'The Cursed Dungeon'},
             'The Abandoned Bedroom': {'North': 'The Majestic Dining Room', 'East': 'The Forgotten Library'},
             'The Forgotten Library': {'East': 'The Abandoned Bedroom'}
             }
    room_items = {'Entrance Hall': [torch_item]}
    room_mobs = {'Entrance Hall': []}

    show_instructions()

    while player.is_alive:
        hud(player, room_mobs, room_items)

        command = input('Enter your move:').split()
        action = command[0].lower()

        if action == 'go':
            player.move(command[1], rooms)


# Sample function showing the goal of the game and move commands
def show_instructions():  # ! NEEDS TO BE REWRITTEN TO MATCH MY GAME
    # print a main menu and the commands
    print("The Depths")
    print("Adventure into the depths and slay the dragon.")
    print("Move commands: go South, go North, go East, go West")
    print("Add to Inventory: get 'item name'")


def hud(player, room_mobs, room_items):
    print(f'You are in {player.location}')
    for mob in room_mobs[player.location]:
        print(f'{mob.name}, Health: {mob.health}')
    for item in room_items[player.location]:
        print(f'{item.name}')

    print(f'Inventory : {player.inventory}')
    print('-------------------------------------')

main()
