from typing import Optional, List, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import *

class AkiongLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        teleport, redbutton = findTeleportandRedButton(board.game_objects)

        target, is_teleport = findTarget(board_bot, teleport, board.diamonds, redbutton, board)

        if not is_teleport:
            target = ignoreTeleport(board_bot.position, teleport, target, board)

        if target is board_bot.position:
            target = board_bot.properties.base

        props = board_bot.properties
        if props.diamonds == props.inventory_size:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            self.goal_position = None

        current_position = board_bot.position

        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                target.x,
                target.y,
            )

        if delta_x == 0 and delta_y == 0:
            delta_x, delta_y = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        return delta_x, delta_y