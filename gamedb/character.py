"""
A character is a fictional person in a game.
A character has a name, a character type, and characteristics.
A character can move around a map, and perform actions.
"""

from gamedb.map import Node

import gamedb.char_types as ctyp


class Character():
    def __init__(self, name: str, char_type: str, location: Node):
        if not isinstance(name, str):
            raise TypeError(f'Bad type for name: {type(name)}')
        if not isinstance(char_type, str):
            raise TypeError(f'Bad type for char_type: {type(char_type)}')
        if not ctyp.exists(char_type):
            raise ValueError(f'Character type {char_type} does not exist.')
        if not isinstance(location, Node):
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

    def move(self, destination: Node):
        if not isinstance(destination, Node):
            raise TypeError(f'Bad type for destination: {type(destination)}')
        self.location = destination

    def add_item(self, item):
        pass


def main():
    # Test Action
    TEST_ACT = {'act_func': lambda x: x, 'act_obj': 'obj'}

    # Test Node
    courtyard = Node('Courtyard', {'test_act': TEST_ACT})
    fountain = Node('Fountain', {'test_act': TEST_ACT})

    # Test Character
    ym = Character('ym', 'Wizard', courtyard)
    print('name: ', ym.get_name())
    print('type: ', ym.get_char_type())
    print('details: ', ym.get_detail_dict())

    # Test move
    print('location: ', ym.get_location().get_descr())
    ym.move(fountain)
    print('location: ', ym.get_location().get_descr())


if __name__ == '__main__':
    main()
