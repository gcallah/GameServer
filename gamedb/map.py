
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
    print(f'{item} added to {character.get_name()}')
    character.add_item(item)
    return SUCCESS


def move(character, node):
    """
    Moves a character to a node.
    """
    print(f'{character.get_name()} {node.get_descr()}')
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
    def __init__(self, graph: dict = {}):
        if not isinstance(graph, dict):
            raise TypeError(f'Bad type for graph: {type(graph)}')
        for node, neighbor_list in graph.items():
            if not isinstance(node, Node):
                raise TypeError(f'Bad type for node: {type(node)}')
            if not isinstance(neighbor_list, list):
                raise TypeError(
                    f'Bad type for neighbor_list: {type(neighbor_list)}')
            for neighbor in neighbor_list:
                if not isinstance(neighbor, Node):
                    raise TypeError(f'Bad type for neighbor: {type(neighbor)}')
        self.graph = graph

    def add(self, src, dest):
        if not isinstance(src, Node):
            raise TypeError(f'Bad type for src: {type(src)}')
        if not isinstance(dest, Node):
            raise TypeError(f'Bad type for dest: {type(dest)}')
        if src not in self.graph:
            self.graph[src] = []
        if dest not in self.graph[src]:
            self.graph[src].append(dest)

    def get_node_list(self):
        return list(self.graph.keys())

    def get_neighbors(self, node):
        if node not in self.graph:
            raise ValueError(f'No such node: {node}')
        return self.graph[node]


PICK_UP_SWORD = 'Pick up sword'
GO_THROUGH_DOOR = 'Go through the door'
TAME_HORSE = 'Tame the horse'
KILL_HORSE = 'Kill the horse'

GRASSY_FIELD_ACTIONS = {
    TAME_HORSE: {
        ACT_FUNC: add,
        ACT_OBJ: 'horse',
    },
    KILL_HORSE: {
        ACT_FUNC: add,
        ACT_OBJ: 'meat',
    },
    # GO_THROUGH_DOOR: {
    #     ACT_FUNC: move,
    #     ACT_OBJ: dark_chamber,
    # },
}

grassy_field = Node('on a grassy field. '
                    + 'There is a friendly horse, and a door behind you.',
                    GRASSY_FIELD_ACTIONS)


DARK_CHAMBER_ACTIONS = {
    PICK_UP_SWORD: {
        ACT_FUNC: add,
        ACT_OBJ: 'sword',
    },
    GO_THROUGH_DOOR: {
        ACT_FUNC: move,
        ACT_OBJ: grassy_field,
    },
}

dark_chamber = Node('in a dark chamber. '
                    + 'There is a sword on the floor, and a door before you.',
                    DARK_CHAMBER_ACTIONS)


def main():
    pass


if __name__ == '__main__':
    main()
