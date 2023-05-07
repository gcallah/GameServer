
"""
A map is a number of locations (nodes) in a network (graph),
with links (edges) between them.
"""

SUCCESS = 0
ERROR = -1

ACT_FUNC = 'act_func'
ACT_OBJ = 'act_obj'


def add(character, item):
    """
    Add an item to a character.
    """
    print(f'{item} added to {character})')
    character.add_item(item)
    return SUCCESS


def move(character, node):
    """
    Moves a character to a node.
    """
    print(f'{character} moved to {node})')
    character.move(node)
    return SUCCESS


class Node():
    """
    descr: describes where a character is on the map.
    actions: a dictionary mapping the description of an action to a function.
    """
    def __init__(self, descr: str, actions: dict):
        self.descr = descr
        if not isinstance(actions, dict):
            raise TypeError(f'Bad type for actions: {type(actions)}')
        self.actions = actions

    def get_descr(self):
        return self.descr

    def get_action_list(self):
        return list(self.actions.keys())

    def get_action_menu(self):
        act_list = list(self.actions.keys())
        menu = '\n'
        choice = 0
        for action in act_list:
            menu += f'{choice}. {action}\n'
            choice += 1
        return menu

    def perform_action(self, act_name, character):
        if act_name not in self.actions:
            raise ValueError(f'No such action: {act_name}')
        else:
            action = self.actions[act_name]
            return action[ACT_FUNC](character, action[ACT_OBJ])


class Map():
    def __init__(self):
        pass


PICK_UP_SWORD = 'Pick up sword'
GO_THROUGH_DOOR = 'Go through the door'


other_location = Node('on a grassy field', {})


ACTIONS = {
    PICK_UP_SWORD: {
        ACT_FUNC: add,
        ACT_OBJ: 'sword',
    },
    GO_THROUGH_DOOR: {
        ACT_FUNC: move,
        ACT_OBJ: other_location,
    },
}


location = Node('in a dark chamber. '
                + 'There is a sword on the floor, and a door before you.',
                ACTIONS)


def main():
    print(f'You are {location.get_descr()}')
    print(f'Your choices are: {location.get_action_menu()}')
    # Here we will take input and execute an action.


if __name__ == '__main__':
    main()
