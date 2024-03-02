from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position 
from typing import Optional
from ..util import get_direction
import random


class PatLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        # Gather game objects
        teleport = [x for x in board.game_objects if (x.type == "TeleportGameObject")]
        blue_diamonds = [x for x in board.game_objects if x.type == "DiamondGameObject" and x.properties.points == 1]
        red_diamonds = [x for x in board.game_objects if x.type == "DiamondGameObject" and x.properties.points == 2]

        # Group teleporters by their pair_id
        teleport_groups = {}
        for teleporter in teleport:
            pair_id = teleporter.properties.pair_id
            if pair_id not in teleport_groups:
                teleport_groups[pair_id] = []
            teleport_groups[pair_id].append(teleporter)

        # Calculate distances
        def calc_distance(obj):
            if isinstance(obj, GameObject):
                return abs(current_position.x - obj.position.x) + abs(current_position.y - obj.position.y)
            elif isinstance(obj, Position):
                return abs(current_position.x - obj.x) + abs(current_position.y - obj.y)

        # Sort each group of teleporters by their distance to the bot and store the distance
        sorted_teleport_groups = {}
        for pair_id, teleporters in teleport_groups.items():
            sorted_teleporters = sorted([(teleporter.position, abs(current_position.x - teleporter.position.x) + abs(current_position.y - teleporter.position.y)) for teleporter in teleporters], key=lambda t: t[1])
            sorted_teleport_groups[pair_id] = sorted_teleporters

        # Sort the sorted_teleport_groups dictionary based on the distance of the nearest teleporter in each group
        sorted_teleport_groups = dict(sorted(sorted_teleport_groups.items(), key=lambda item: item[1][0][1]))
        # Sort blue and red diamonds by their distance to the bot, and store the distance
        blue_sorted = sorted([(diamond, calc_distance(diamond)) for diamond in blue_diamonds], key=lambda t: t[1])
        red_sorted = sorted([(diamond, calc_distance(diamond)) for diamond in red_diamonds], key=lambda t: t[1])
        print(blue_sorted)
        print(red_sorted)

        # Set goal position based on conditions
        if props.diamonds >= 5:
            self.goal_position = props.base
        elif props.diamonds == 4:
            self.goal_position = blue_sorted[0][0].position if blue_sorted else props.base
        elif red_sorted and (not blue_sorted or red_sorted[0][1] <= blue_sorted[0][1]):
            self.goal_position = red_sorted[0][0].position
        elif props.milliseconds_left < 10000 and props.diamonds >= 2:
            self.goal_position = props.base
        elif blue_sorted:
            self.goal_position = blue_sorted[0][0].position
        else:
            self.goal_position = props.base

        # Find the shortest way using teleporters
        if self.goal_position:
            direct_distance = calc_distance(self.goal_position)
            shortest_way = direct_distance
            shortest_way_position = self.goal_position
            for pair_id, teleporters in sorted_teleport_groups.items():
                closest_teleporter, distance_to_closest_teleporter = teleporters[0]
                second_teleporter = teleporters[1][0]
                # Calculate the distance from the second teleporter in the pair to the goal position
                distance_tele2_goal = calc_distance(second_teleporter)

                if distance_tele2_goal < direct_distance :
                    way1 = distance_to_closest_teleporter + distance_tele2_goal
                    if way1 < shortest_way:
                        shortest_way = way1
                        shortest_way_position = closest_teleporter
                
        self.goal_position = shortest_way_position

        delta_x, delta_y = 0, 0
        if current_position == self.goal_position:
            # If the bot is at the goal position, choose a random direction to move
            delta_x, delta_y = random.choice(self.directions)
        else:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y