import random
from typing import Optional, List, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

THRESHOLD_TIME = 10

def findTeleportandRedButton(game_objects: List[GameObject]):
    teleport_pairs = {}
    redbutton = None
    for game_object in game_objects:
        if game_object.type == 'TeleportGameObject':
            pair_id = game_object.properties.pair_id
            position = game_object.position
            if pair_id in teleport_pairs:
                teleport_pairs[pair_id].append(position)
            else:
                teleport_pairs[pair_id] = [position]
        elif game_object.type == 'DiamondButtonGameObject':
            redbutton = game_object.position

    return [(pair[0], pair[1]) for pair in teleport_pairs.values() if len(pair) == 2], redbutton

def findDistance(current: Position, teleport: List[Tuple[Position, Position]], target: Position):
    direct_distance = abs(current.x - target.x) + abs(current.y - target.y)
    if not teleport:
        return target, direct_distance, False
    min_teleport_distance = float('inf')
    teleport_entry = None
    for pair in teleport:
        for portal in pair:
            distance_to_portal = abs(current.x - portal.x) + abs(current.y - portal.y)
            other_portal = pair[0] if portal == pair[1] else pair[1]
            distance_from_other_portal_to_target = abs(other_portal.x - target.x) + abs(other_portal.y - target.y)
            total_teleport_distance = distance_to_portal + distance_from_other_portal_to_target
            if total_teleport_distance < min_teleport_distance:
                min_teleport_distance = total_teleport_distance
                teleport_entry = portal
    if min_teleport_distance < direct_distance:
        return teleport_entry, min_teleport_distance, True
    else:
        return target, direct_distance, False

class V1Logic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        teleport, redbutton = findTeleportandRedButton(board.game_objects)
        props = board_bot.properties
        current_position = board_bot.position
        if props.diamonds == props.inventory_size:
            self.goal_position = board_bot.properties.base
        else:
            closest_diamond = None
            min_distance = float('inf')
            for diamond in board.diamonds:
                distance = findDistance(current_position, teleport, diamond.position)[1]
                if distance < min_distance:
                    min_distance = distance
                    closest_diamond = diamond.position
            self.goal_position = closest_diamond
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            delta_x, delta_y = 0, 0
        if delta_x == 0 and delta_y == 0:
            delta_x, delta_y = random.choice(self.directions)

        return delta_x, delta_y