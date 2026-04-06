from enum import IntEnum
import os
import time

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

direction_symbols = {
    '^': Direction.NORTH,
    '>': Direction.EAST,
    'V': Direction.SOUTH,
    '<': Direction.WEST
}

EMPTY_POSITION = (None, None)

def add_to_dict_list(dictionary: dict[any, list], item, value):
    if item in dictionary:
        dictionary[item].append(value)
    else:
        dictionary[item] = [ value ]

def add_to_dict_set(dictionary: dict[any, set], item, value):
    if item in dictionary:
        dictionary[item].add(value)
    else:
        dictionary[item] = { value }

def rot_90(currentDirection: Direction) -> Direction:
    return Direction((int(currentDirection) + 1) % 4)

def read_file(file_name):
    file_name = file_name if file_name.endswith(".txt") else f'{file_name}.txt'
    currentFilePath = os.path.abspath(f'{os.path.dirname(__file__)}/{file_name}')

    with open(currentFilePath, mode="r") as file:
        return file.read().split("\n")

def process_map(map: list[str]):
    obs_cols = dict[int, list]()
    obs_rows = dict[int, list]()
    guard_position = None
    guard_direction = None

    for row in range(len(map)):
        for col in range(len(map[0])):
            match map[row][col]:
                case ".":
                    continue
                case "#":
                    add_to_dict_list(obs_cols, col, row)
                    add_to_dict_list(obs_rows, row, col)
                case "^" | ">" | "V" | "<":
                    guard_direction = direction_symbols[map[row][col]]
                    guard_position = (row, col)
            
    return (obs_cols, obs_rows, guard_position, guard_direction)    

def find_array_position(array: list, value):
    '''
    Helper function to find the position of a value in a sorted array using binary search.
    Returns the index of the value if found, or the index where it would be inserted if not found.
    '''
    left, right = 0, len(array)

    while left < right:
        mid = (left + right) // 2
        if array[mid] < value:
            left = mid + 1
        else:
            right = mid

    return left

def determine_guard_positions(file_name):
    map = read_file(file_name)
    start = time.time()

    obs_cols, obs_rows, guard_position, guard_direction = process_map(map)
    start_position = guard_position

    def is_on_map(position: tuple[int, int]) -> bool:
        row, col = position
        return row >= 0 and row < len(map) and col >= 0 and col < len(map[0])

    def get_next_obstacle(guard_direction: Direction, guard_position: tuple[int, int]):
        next_obs_exists = True
        row, col = guard_position
        obs_row, obs_col = EMPTY_POSITION
        next_position = EMPTY_POSITION

        obstacle_line = None
        is_positive_direction = guard_direction == Direction.SOUTH or guard_direction == Direction.EAST

        match guard_direction:
            case Direction.NORTH | Direction.SOUTH:
                obstacle_line = obs_cols.get(col)
                obs_col = col
            case Direction.EAST | Direction.WEST:
                obstacle_line = obs_rows.get(row)
                obs_row = row

        if obstacle_line is not None and len(obstacle_line) != 0:
            guards_pos_in_line = find_array_position(obstacle_line, row if guard_direction in (Direction.NORTH, Direction.SOUTH) else col)

            if is_positive_direction:
                if guards_pos_in_line < len(obstacle_line):
                    if guard_direction == Direction.SOUTH:
                        obs_row = obstacle_line[guards_pos_in_line]
                        next_position = (obs_row - 1, obs_col)
                    else:
                        obs_col = obstacle_line[guards_pos_in_line]
                        next_position = (obs_row, obs_col - 1)
            else:
                if guards_pos_in_line > 0:
                    if guard_direction == Direction.NORTH:
                        obs_row = obstacle_line[guards_pos_in_line-1]
                        next_position = (obs_row + 1, obs_col)
                    else:
                        obs_col = obstacle_line[guards_pos_in_line-1]
                        next_position = (obs_row, obs_col + 1)

        # set next_obs_exists to false if no obstacle is found in the direction of movement
        # and set the obstacle position to be just outside the map in the direction of movement
        if obs_row == EMPTY_POSITION[0]:
            next_obs_exists = False
            obs_row = -1 if guard_direction == Direction.NORTH else len(map)
            next_position = (obs_row, obs_col)
        if obs_col == EMPTY_POSITION[1]:
            next_obs_exists = False
            obs_col = -1 if guard_direction == Direction.WEST else len(map[0])
            next_position = (obs_row, obs_col)
        
        next_obstacle = (obs_row, obs_col)
        return next_obs_exists, next_obstacle, next_position

    def step_forward(position: tuple[int, int], direction: Direction):
        match direction:
            case Direction.NORTH:
                return (position[0]-1, position[1])
            case Direction.SOUTH:
                return (position[0]+1, position[1])
            case Direction.EAST:
                return (position[0], position[1]+1)
            case Direction.WEST:
                return (position[0], position[1]-1)
            case _:
                return position

    def has_loop(
        position: tuple[int, int], 
        direction: Direction, 
        found_obstacles: dict, 
        explored: dict) -> bool:

        #simulate adding new obstacle
        added_obs = step_forward(position, direction)
        if (not is_on_map(added_obs) 
            or added_obs == start_position 
            or map[added_obs[0]][added_obs[1]] == "#"
            or added_obs in explored):
            return False
        
        add_to_dict_list(obs_rows, added_obs[0], added_obs[1])
        add_to_dict_list(obs_cols, added_obs[1], added_obs[0])
        obs_rows[added_obs[0]].sort()
        obs_cols[added_obs[1]].sort()
        add_to_dict_list(found_obstacles, added_obs, direction)

        loop_found = False
        next_obs_exists = True
        curr_position = position
        curr_direction = direction
        path_explored = dict()
        while next_obs_exists:
            curr_direction = rot_90(curr_direction)
            next_obs_exists, nextObs, curr_position = get_next_obstacle(curr_direction, curr_position)

            if (curr_direction in found_obstacles.get(nextObs, {})
                or curr_direction in path_explored.get(curr_position, {})):
                loop_found = True
                break

            add_to_dict_set(path_explored, curr_position, curr_direction)
        
        #undo simulation
        obs_rows[added_obs[0]].remove(added_obs[1])
        obs_cols[added_obs[1]].remove(added_obs[0])
        found_obstacles.pop(added_obs)
        return loop_found

    def add_path_to_next_obstacle(position, direction, explored: dict, found_obstacles: dict):
        num_loops = 0
        next_obs_exists, next_obstacle, next_position = get_next_obstacle(direction, position)
        curr_position = position

        while curr_position != next_position:
            if has_loop(curr_position, direction, found_obstacles, explored):
                num_loops += 1   
            curr_position = step_forward(curr_position, direction)
            add_to_dict_set(explored, curr_position, direction)
                   
        if next_obs_exists:
            add_to_dict_set(found_obstacles, next_obstacle, direction)

        return next_obs_exists, next_position, num_loops

    # find guard positions
    explored_positions = dict()
    found_obstacles = dict()
    next_obs_exists = True
    possible_loops = 0
    while is_on_map(guard_position) and next_obs_exists:
        next_obs_exists, guard_position, num_loops = add_path_to_next_obstacle(guard_position, guard_direction, explored_positions, found_obstacles)
        guard_direction = rot_90(guard_direction)
        possible_loops += num_loops
        #print(guard_position, guard_direction, num_loops, next_obs_exists)
    
    print(
f"""Time taken: {time.time() - start:.2f}
Guard positions: {len(explored_positions)}
Possible loops: {possible_loops}"""
    )

# determine_guard_positions("example")
# determine_guard_positions("input")
determine_guard_positions("../inputs/day6")