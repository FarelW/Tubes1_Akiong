import random
from typing import Optional,List,Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def findTeleportandRedButton(game_objects:List[GameObject]):
    teleport_pairs = {}
    redbutton=None
    for game_object in game_objects:
        if game_object.type == 'TeleportGameObject':
            pair_id = game_object.properties.pair_id
            position = game_object.position
            if pair_id in teleport_pairs:
                teleport_pairs[pair_id].append(position)
            else:
                teleport_pairs[pair_id] = [position]
        elif game_object.type == 'DiamondButtonGameObject':
            redbutton=game_object.position

    return [(pair[0], pair[1]) for pair in teleport_pairs.values() if len(pair) == 2],redbutton

def findDistance(current:Position,teleport:List[Tuple[Position,Position]],target:Position):
    tp_close_to_current=[None for i in range(len(teleport))]
    distance_to_tp=[100 for i in range (len(teleport))]
    otherside_tp=[None for i in range (len(teleport))]
    otherside_tp_to_target=[100 for i in range (len(teleport))]

    for i in range(len(teleport)):
        for j in range (2):
            total=abs(teleport[i][j].x-current.x)+abs(teleport[i][j].y-current.y)
            if total<distance_to_tp[i] and total!=0:
                distance_to_tp[i]=total
                tp_close_to_current[i]=teleport[i][j]
                for k in range (2):
                    if k!=j:
                        otherside_tp[i]=teleport[i][k]
                        other=abs(teleport[i][k].x-target.x)+abs(teleport[i][k].y-target.y)
                        otherside_tp_to_target[i]=other

    tp_most_efficient=100
    tp_entry=None
    for i in range (len(teleport)):
        if distance_to_tp[i]+otherside_tp_to_target[i]<tp_most_efficient:
            tp_most_efficient=distance_to_tp[i]+otherside_tp_to_target[i]
            tp_entry=tp_close_to_current[i]

    current_to_target=abs(current.x-target.x)+abs(current.y-target.y)
    
    if tp_most_efficient>current_to_target:
        distance=current_to_target
        return target,distance,False
    else:
        distance=tp_most_efficient
        return tp_entry,distance,True

# def findTarget(current: GameObject,teleport: List[Tuple[Position,Position]],diamond:List[GameObject],board:Board):
#     distance_diamond_blue=100
#     distance_diamond_red=100
#     target_blue=None
#     target_red=None
#     is_tp_red=False
#     is_tp_blue=False

#     for i in range(len(diamond)):
#         if diamond[i].properties.points==1:
#             temp_target,temp_distance,temp_tp=findDistance(current.position,teleport,diamond[i].position)
#             if temp_distance<distance_diamond_blue:
#                 distance_diamond_blue=temp_distance
#                 target_blue=temp_target
#                 is_tp_blue=temp_tp
#         else:
#             temp_target,temp_distance,temp_tp=findDistance(current.position,teleport,diamond[i].position)
#             if temp_distance<distance_diamond_red:
#                 distance_diamond_red=temp_distance
#                 target_red=temp_target
#                 is_tp_red=temp_tp
    
#     if target_red:
#         base_target,distance_base_red,_=findDistance(target_red,teleport,current.properties.base)
#     if target_blue:
#         base_target,distance_base_blue,_=findDistance(target_blue,teleport,current.properties.base)

#     base_target,_,is_back_tp=findDistance(current.position,teleport,current.properties.base)

#     if distance_diamond_blue<distance_diamond_red-round(board.width/3):
#         # if distance_base_blue+distance_diamond_blue>round(current.properties.milliseconds_left/1000):
#         #     return base_target,is_back_tp
#         # else:
#             return target_blue,is_tp_blue
#     else:
#         # if distance_base_red+distance_diamond_red>round(current.properties.milliseconds_left/1000):
#         #     return base_target,is_back_tp
#         # else:
#             if current.properties.diamonds<current.properties.inventory_size-1:
#                 return target_red,is_tp_red
#             else:
#                 # if distance_base_blue+distance_diamond_blue>round(current.properties.milliseconds_left/1000):
#                 #     return base_target,is_back_tp
#                 # else:
#                     return target_blue,is_tp_blue

# def findQuadran(current:Position,target:Position):
#     # 10 means vertically, -10 means horizontally
#     direction_quadran=10
#     if current.x>target.x:
#         if current.y>target.y:
#             direction_quadran=2
#         elif current.y<target.y:
#             direction_quadran=3
#         else:
#             direction_quadran=-10
#     elif current.x<target.x:
#         if current.y>target.y:
#             direction_quadran=1
#         elif current.y<target.y:
#             direction_quadran=4
#         else:
#             direction_quadran=-10
    
#     return direction_quadran

# def isTeleportInterupt(current:Position,teleport:Position,target:Position):
#     quadran=findQuadran(current,target)
    
#     if quadran==10:
#         if current.x==teleport.x and current.x==target.x:
#             if current.y>target.y:
#                 if teleport.y<current.y and teleport.y>target.y:
#                     return True,quadran
#                 else:
#                     return False,quadran
#             else:
#                 if teleport.y>current.y and teleport.y<target.y:
#                     return True,quadran
#                 else:
#                     return False,quadran
#         else:
#             return False,quadran
    
#     elif quadran==-10:
#         if current.y==teleport.y and current.y==target.y:
#             if current.x>target.x:
#                 if teleport.x<current.x and teleport.x>target.x:
#                     return True,quadran
#                 else:
#                     return False,quadran
#             else:
#                 if teleport.x>current.x and teleport.x<target.x:
#                     return True,quadran
#                 else:
#                     return False,quadran
#         else:
#             return False,quadran
    
#     else:
#         if current.y==teleport.y:
#             if quadran==1 or quadran==4:
#                 if teleport.x>current.x and teleport.x<target.x:
#                     return True,quadran
#                 else:
#                     return False,quadran
#             elif quadran==2 or quadran==3:
#                 if teleport.x>current.x and teleport.x<target.x:
#                     return True,quadran
#                 else:
#                     return False,quadran
#         else:
#             if teleport.x==target.x:
#                 if quadran==1 or quadran==2:
#                     if teleport.y<current.y and teleport.y>target.y:
#                         return True,quadran
#                     else:
#                         return False,quadran
#                 elif quadran==3 or quadran==4:
#                     if teleport.y>current.y and teleport.y<target.y:
#                         return True,quadran
#                     else:
#                         return False,quadran
#             else:
#                 return False,quadran
            
# def ignoreTeleport(current:Position,teleport:List[Tuple[Position,Position]],target:Position, board:Board):
    result:Position=target

    is_teleport_interupt,quadran=False,None
    teleport_crash=None

    for i in range (len(teleport)):
        for j in range(2):
            temp_will,temp_quadran=isTeleportInterupt(current,teleport[i][j],target)
            if temp_will==True:
                teleport_crash=teleport[i][j]
                is_teleport_interupt=temp_will
                quadran=temp_quadran
                break

    if is_teleport_interupt:
        if quadran==10:
            if current.x==0:
                result.x=current.x+1
                result.y=current.y
            elif current.x==board.width-1:
                result.x=current.x-1
                result.y=current.y
            else:
                result.x=random.choice([current.x+1, current.x-1])
                result.y=current.y
        elif quadran==-10:
            if current.y==0:
                result.x=current.x
                result.y=current.y+1
            elif current.y==board.height-1:
                result.x=current.x
                result.y=current.y-1
            else:
                result.x=current.x
                result.y=random.choice([current.y+1, current.y-1])
        elif quadran==1:
            if current.x==teleport_crash.x-1:
                result.x=current.x
                result.y=current.y-1
            elif current.x==teleport_crash.x:
                result.x=current.x
                result.y=current.y-1
        elif quadran==2:
            if current.x==teleport_crash.x+1:
                result.x=current.x
                result.y=current.y-1
            elif current.x==teleport_crash.x:
                result.x=current.x
                result.y=current.y-1
        elif quadran==3:
            if current.x==teleport_crash.x+1:
                result.x=current.x
                result.y=current.y+1
            elif current.x==teleport_crash.x:
                result.x=current.x
                result.y=current.y+1
        elif quadran==4:
            if current.x==teleport_crash.x-1:
                result.x=current.x
                result.y=current.y+1
            elif current.x==teleport_crash.x:
                result.x=current.x
                result.y=current.y+1
    
    print("current:",current,"result:",result,"is:",is_teleport_interupt,"quadaran:",quadran)

    return result

def findCluster(current:GameObject,teleport: List[Tuple[Position,Position]],redbutton:Position,board:Board):
    most=-1000
    target=redbutton
    _,distance_button,_=findDistance(current.position,teleport,redbutton)
    for i in range(len(board.diamonds)):
        diamond_now=board.diamonds[i].position
        _,distance,_=findDistance(current.position,teleport,diamond_now)
        count=0
        for j in range(len(board.diamonds)):
            diamond_temp=board.diamonds[j].position
            if ((diamond_temp.x<diamond_now.x+round(board.width/5) or 
                 diamond_temp.x<diamond_now.x-round(board.width/5)) and 
                 (diamond_temp.y<diamond_now.y+round(board.height/5) or 
                  diamond_temp.y<diamond_now.y-round(board.width/5))
                  and i!=j):
                count+=1

        if -distance+count>most:
            _,diamond_to_home,_=findDistance(diamond_now,teleport,current.properties.base)
            _,now_to_base,_=findDistance(current.position,teleport,current.properties.base)
            if current.properties.diamonds>=round(current.properties.inventory_size/2):
                if distance>now_to_base:
                    target=current.properties.base
                else:
                    if distance<=distance_button:
                        if board.diamonds[i].properties.points==2:
                            if current.properties.diamonds<current.properties.inventory_size-1:
                                # if distance+diamond_to_home<=round(current.properties.milliseconds_left/1000):
                                    most=-distance+count
                                    target=board.diamonds[i].position
                                # else:
                                #     if current.position!=current.properties.base:
                                #         target=current.properties.base
                                #     else:
                                #         target=redbutton
                        else:
                            # if distance+diamond_to_home<=round(current.properties.milliseconds_left/1000):
                                most=-distance+count
                                target=board.diamonds[i].position
                            # else:
                            #     if current.position!=current.properties.base:
                            #         target=current.properties.base
                            #     else:
                            #         target=redbutton
                    else:
                        target=redbutton
            else:
                if distance<distance_button+1:
                    if board.diamonds[i].properties.points==2:
                        if current.properties.diamonds<current.properties.inventory_size-1:
                            # if distance+diamond_to_home<=round(current.properties.milliseconds_left/1000):
                                most=-distance+count
                                target=board.diamonds[i].position
                            # else:
                            #     if current.position!=current.properties.base:
                            #         target=current.properties.base
                            #     else:
                            #         target=redbutton
                    else:
                        # if distance+diamond_to_home<=round(current.properties.milliseconds_left/1000):
                            most=-distance+count
                            target=board.diamonds[i].position
                        # else:
                        #     if current.position!=current.properties.base:
                        #         target=current.properties.base
                        #     else:
                        #         target=redbutton
                else:
                    target=redbutton


    return target

class MainLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        teleport,redbutton=findTeleportandRedButton(board.game_objects)

        target=findCluster(board_bot,teleport,redbutton,board)

        # if not is_teleport:
            # target=ignoreTeleport(board_bot.position,teleport,target,board)

        props = board_bot.properties
        print(props.milliseconds_left)
        print(board_bot.properties.score)
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
