"""
A character is a fictional person in a game.
A character has a name, a character type, and characteristics.
A character can move around a map, and perform actions.
"""

import gamedb.map as map

import gamedb.char_types as ctyp


class Character():
    def __init__(self, name: str, char_type: str, location: map.Node):
        if not isinstance(name, str):
            raise TypeError(f'Bad type for name: {type(name)}')
        if not isinstance(char_type, str):
            raise TypeError(f'Bad type for char_type: {type(char_type)}')
        if not ctyp.exists(char_type):
            raise ValueError(f'Character type {char_type} does not exist.')
        if not isinstance(location, map.Node):
            raise TypeError(f'Bad type for location: {type(location)}')
        self.name = name
        self.char_type = char_type
        self.details = ctyp.get_char_type_details(self.char_type)
        self.location = location
        self.items = []

    def get_name(self):
        return self.name

    def get_char_type(self):
        return self.char_type

    def get_location(self):
        return self.location

    def get_detail_dict(self):
        return self.details

    def get_detail(self, detail_name):
        return self.details[detail_name]

    def set_detail(self, detail_name, detail_value):
        if not isinstance(detail_name, str):
            raise TypeError(f'Bad type for ability_name: {type(detail_name)}')
        if not isinstance(detail_value, int):
            raise TypeError(
                f'Bad type for ability_value: {type(detail_value)}')
        self.details[detail_name] = detail_value

    def move(self, destination: map.Node):
        if not isinstance(destination, map.Node):
            raise TypeError(f'Bad type for destination: {type(destination)}')
        self.location = destination

    def add_item(self, item):
        self.items.append(item)


def main():
    # New character
    character = Character('Bob', 'Warrior', map.dark_chamber)
    print(f'You are {character.get_name()} the {character.get_char_type()}')
    print(f'You are {character.get_location().get_descr()}')

    # Start the game
    print(f'Your choices are: {character.get_location().get_action_menu()}')
    choice = int(input('What do you do? Enter 999 to quit.'))

    while choice != 999:
        location = character.get_location()
        act_name = location.get_action_list()[choice]
        print(f'You chose: {act_name}')
        if location.perform_action(act_name, character) == map.SUCCESS:
            print(f'Action {act_name} succeeded.')
        else:
            print(f'Action {act_name} failed.')
        print(
            f'Your choices are: {character.get_location().get_action_menu()}')
        choice = int(input('What do you do? Enter 999 to quit.'))

    print('Goodbye!')


if __name__ == '__main__':
    main()
