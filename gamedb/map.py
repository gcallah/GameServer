
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
    return SUCCESS


def move(character, node):
    """
    Moves a character to a node.
    """
    print(f'{character} moved to {node})')
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

    def perform_action(self, act_name, character):
        if act_name not in self.actions:
            raise ValueError(f'No such action: {act_name}')
        else:
            action = self.actions[act_name]
            return action[ACT_FUNC](character, action[ACT_OBJ])


class Map():
    def __init__(self):
        pass
