# Daniel Aguiar

def main():
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
    show_instructions()


# Sample function showing the goal of the game and move commands
def show_instructions():  # ! NEEDS TO BE REWRITTEN TO MATCH MY GAME
    # print a main menu and the commands
    print("Dragon Text Adventure Game")
    print("Collect 6 items to win the game, or be eaten by the dragon.")
    print("Move commands: go South, go North, go East, go West")
    print("Add to Inventory: get 'item name'")


main()
