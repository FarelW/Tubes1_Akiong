import random
from typing import Optional,List,Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def findRedButton(game_objects: List[GameObject]):
    redbutton = None
    for game_object in game_objects:
        if game_object.type == 'DiamondButtonGameObject':
            redbutton = game_object.position

    return redbutton

def isNearBase(position: Position, base: Position, board: Board) -> bool:
    # Calculate the bounds of the 6x6 area around the base
    x_min = max(base.x - 3, 0)
    x_max = min(base.x + 2, board.width - 1)
    y_min = max(base.y - 3, 0)
    y_max = min(base.y + 2, board.height - 1)

    # Adjust the bounds if the area goes beyond the board's boundaries
    if x_max - x_min < 5:
        if x_min == 0:
            x_max = min(5, board.width - 1)
        else:
            x_min = max(board.width - 6, 0)

    if y_max - y_min < 5:
        if y_min == 0:
            y_max = min(5, board.height - 1)
        else:
            y_min = max(board.height - 6, 0)

    # Check if the position is within the 6x6 area around the base
    return x_min <= position.x <= x_max and y_min <= position.y <= y_max

def findDiamondNearBase(current: GameObject, diamond: List[GameObject], board: Board):
    arraydiamond = []
    fardiamond= []
    home = current.properties.base

    # Calculate the bounds of the 6x6 area around the base
    x_min = max(home.x - 3, 0)
    x_max = min(home.x + 2, board.width - 1)
    y_min = max(home.y - 3, 0)
    y_max = min(home.y + 2, board.height - 1)

    # Adjust the bounds if the area goes beyond the board's boundaries
    if x_max - x_min < 5:
        if x_min == 0:
            x_max = min(5, board.width - 1)
        else:
            x_min = max(board.width - 6, 0)

    if y_max - y_min < 5:
        if y_min == 0:
            y_max = min(5, board.height - 1)
        else:
            y_min = max(board.height - 6, 0)

    for d in diamond:
        if x_min <= d.position.x <= x_max and y_min <= d.position.y <= y_max:
            arraydiamond.append(d.position)
        else:
            fardiamond.append(d.position)

    return arraydiamond,fardiamond

def findClosestDiamond(current:Position,diamond:List[Position]):
    closest=10000
    target=None
    for i in range (len(diamond)):
        tot=abs(diamond[i].x-current.x)+abs(diamond[i].y-current.y)
        if tot<closest:
            closest=tot
            target=diamond[i]
    
    return closest,target

class TesterLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        redbutton=findRedButton(board.game_objects)
        props = board_bot.properties
        diamondnear,diamondfar=findDiamondNearBase(board_bot,board.diamonds,board)

        print(diamondnear,diamondfar)

        if len(diamondnear)!=0:
            _,target=findClosestDiamond(board_bot.position,diamondnear)
        else:
            if isNearBase(redbutton,board_bot.properties.base,board):
                target=redbutton
            else:
                _,target=findClosestDiamond(board_bot.position,diamondfar)

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
                
        return delta_x, delta_y
