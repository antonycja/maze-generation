import turtle
import random

# min_x, min_y, max_x, max_y = random.choice([(
# -100, -100, 100, 100), (-200, -100, 200, 100), (-100, -200, 100, 200), (-500, -300, 500, 300)])
min_x, min_y, max_x, max_y = -100, -100, 100, 100

# print("box Size", (min_x, min_y, max_x, max_y))

# cell_size = random.choice([10, 20, 25,])
cell_size = random.choice([25])

# print("Cell size", cell_size)


def draw_constraint_box(min_x: int, min_y: int, max_x: int, max_y: int) -> list:
    """Draw the outline box and return the position of each box.

    Args:
        min_x (int): the minimum point on the x axis.
        min_y (int): the minimum point on the y axis.
        max_x (int): the maximum point on the x axis.
        max_y (int): the maximum point on the y axis

    Returns:
        list: list of coordinates (tuples) for the outline box.
    """
    outline_wall = []
    tim = turtle.Turtle(visible=False)
    tim.getscreen().tracer(0)
    tim.pen(speed=0, pendown=False)
    tim.goto(min_x, max_y)

    # top - left to right
    for i in range(min_x, max_x-cell_size, cell_size):
        pos = (i, max_y)
        tim.penup()
        tim.goto(pos)
        tim.pendown()
        draw_square(cell_size, tim, "black", "black")
        outline_wall.append(pos)

    # right - top to bottom
    # left - top to bottom
    for i in range(max_y, min_y+cell_size,  -cell_size):
        pos_right = (max_x-cell_size, i)
        pos_left = (min_x, i)
        tim.penup()
        tim.goto(pos_right)
        tim.pendown()
        draw_square(cell_size, tim, "black", "black")
        outline_wall.append(pos_right)

        tim.penup()
        tim.goto(pos_left)
        tim.pendown()
        draw_square(cell_size, tim, "black", "black")
        outline_wall.append(pos_left)

    # bottom - left to right
    for i in range(min_x, max_x, cell_size):
        pos = (i, min_y+cell_size)
        tim.penup()
        tim.goto(pos)
        tim.pendown()
        draw_square(cell_size, tim, "black", "black")
        outline_wall.append(pos)

    return outline_wall


def draw_square(cell_size: int, turtle_name: str, color="black", pen_color="black") -> list:
    """Draw a square using the given turtle.

    Args:
        cell_size (int): the size(length/steps) of each side of the square.
        turtle_name (str): the name of the turtle to use when drawing.
        color (str, optional): the fill color of the square. Defaults to "black".
        pen_color (str, optional): the outline(pen) color of the box. Defaults to "black".

    Returns:
        turtle.2dVec: a tuple containing the corners of the square.
    """
    turtle_name.begin_poly()
    turtle_name.pen(shown=False, pencolor=pen_color, fillcolor=color, speed=0)
    turtle_name.begin_fill()
    for _ in range(4):
        turtle_name.forward(cell_size)
        turtle_name.right(90)
    turtle_name.end_fill()
    turtle_name.end_poly()
    turtle_name.penup()
    return turtle_name.get_poly()
    pass


def draw_starting_point() -> list:
    """draw the center starting point.

    Returns:
        list(tuple): a list of tuples containing coordinates.
    """
    starting = turtle.Turtle(visible=False)
    starting.getscreen().tracer(0)
    center_starting_pos = []
    starting_y_point = cell_size
    for line in range(1):
        starting_x_point = -cell_size
        for row in range(1):
            starting.begin_poly()
            starting.goto(starting_x_point, starting_y_point)
            draw_square(cell_size, starting, "white", "white")
            starting_x_point += cell_size
            starting.end_poly()
            center_starting_pos.append(starting.get_poly()[0])
        # Drawing down
        starting_y_point -= cell_size

    return center_starting_pos


def fill_in_constraints_box(cell_size: int, min_x: int, max_y: int, vertical_cells: int, horizontal_cells: int) -> list:
    """Fill in the boxes and return a list containing all those positions.

    Args:
        cell_size (int): the size(length/steps) of each side of the square.
        min_x (int): the minimum point on the x axis.
        max_y (int): the maximum point on the x axis.
        vertical_cells (int): the number of squares that can fit in the box vertically.
        horizontal_cells (int): the number of squares that can fit in the box horizontally.

    Returns:
        list: the list of positions available.
    """
    list_of_all_boxes_1d = []
    print("Vertical", vertical_cells)
    print("Horizontal", horizontal_cells)
    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.getscreen().tracer(0)
    t.penup()
    t.goto(min_x, max_y)
    t.pendown()

    for horizontal in range(horizontal_cells):
        for vertical in range(vertical_cells):
            list_of_squares = draw_square(cell_size, turtle_name=t)
            list_of_all_boxes_1d.append(list_of_squares[0])
            t.forward(cell_size)
            pass
        t.right(90)
        t.forward(cell_size)
        t.left(90)
        t.back(vertical_cells*cell_size)

    return list_of_all_boxes_1d

    pass


def choose_random_move_index(current_index: int, x_cells: int, y_cells: int, visited_list: list, stack: list) -> tuple:
    """Choose a random index to move the robot to.

    Args:
        current_index (int): the index of the coordinates that the robot is currently on.
        x_cells (int): the number of squares that can fit in the box horizontally.
        y_cells (int): the number of squares that can fit in the box vertically
        visited_list (list): a list containing all previously visited indexes.
        stack (list): a list that represent a stack containing all the moves being played.

    Returns:
        tuple(int, int): a tuple containing the random index and the random wall index. 
    """

    len_of_obs = (x_cells * y_cells)
    if current_index == None:
        current_index = 0
    # Check the first index, and choose an index to place the wall.
    if current_index == 0:
        down = current_index + x_cells
        right = current_index+1
        list_of_directions = [down, right]

    # Check if the current row is the last row and
    elif (current_index+1) % x_cells == 0 and (current_index+1) < len_of_obs:
        # Check if its on the first line
        if (current_index+1) - x_cells == 0:
            down = current_index + x_cells
            left = current_index - 1
            list_of_directions = [down, left]

        # Check if the current index is the last index
        elif (current_index) == len_of_obs-1:
            up = current_index - x_cells
            left = current_index - 1
            list_of_directions = [up, left]

        # Do the indexes in between
        else:
            up = current_index - x_cells
            down = current_index + x_cells
            left = current_index - 1
            list_of_directions = [up, down, left]

    # Check the first row and choose a random index for the robot to go to.
    elif current_index < x_cells:
        down = current_index + x_cells
        left = right = current_index-1
        right = current_index+1
        list_of_directions = [left, right, down]

    # Check the first row which will always be divisible by the x_cells
    elif current_index % x_cells == 0:

        # Check if that current index is not in the last line
        if (len_of_obs - x_cells) == current_index:
            up = current_index - x_cells
            right = current_index + 1
            list_of_directions = [up, right]
        else:
            down = current_index + x_cells
            up = current_index - x_cells
            right = current_index+1
            list_of_directions = [up, down, right]

    # Check if the current index is in the last row
    elif current_index > (len_of_obs) - x_cells:
        up = current_index - x_cells
        left = right = current_index-1
        right = current_index+1
        list_of_directions = [up, left, right]

    else:
        # All the other options left which is the middle blocks
        up = current_index - x_cells
        down = current_index + x_cells
        left = current_index-1
        right = current_index+1
        list_of_directions = [up, down, left, right]

    in_visited = []
    #  check every possible direction to see if its not already visited.
    for direction in list_of_directions:
        if direction in visited_list:
            in_visited.append(True)
        elif direction < len_of_obs:
            in_visited.append(False)

    while True:
        random_index = random.choice(list_of_directions)
        if random_index not in visited_list:
            # Check if the chosen random number is not already visited and remove it from the list if it was visited.
            list_of_directions.remove(random_index)
            while True:
                # choose a random direction to place the wall and check if its not visited already.
                wall_index = random.choice(list_of_directions)
                if wall_index not in visited_list:
                    break
                # if visited remove and repeat.
                list_of_directions.remove(wall_index)
                if len(list_of_directions) == 0:
                    wall_index = None
                    break
            break
        else:
            if all(in_visited) and len(stack) > 1:
                # Do the stack reverse here

                # print("going back")
                stack.pop()
                random_index = stack[-1]
                wall_index = None
                break
            elif len(stack) == 1 and all(in_visited):
                # Check is the stack only have one value, if so then there are no more possible routes start placing walls where there isn't
                random_index = None
                for i in range(0, len_of_obs):
                    if i not in visited_list:
                        wall_index = i
                        break
                try:
                    if wall_index >= 0:
                        break
                except UnboundLocalError:
                    wall_index = 0
                    pass

    return random_index, wall_index


def is_maze_position_valid(position, visited_list):
    if position not in visited_list:  # The position has not changed
        return True
    else:
        return False
        pass

    pass


def create_maze_route(cell_size, min_x, min_y, max_x, max_y, list_of_all_boxes_1d, center_starting_blocks, outline_wall_pos_list):
    horizontal_cells = int((-min_x + max_x) / cell_size)
    vertical_cells = int((-min_y + max_y) / cell_size)
    maze_route = []
    maze_wall_list = []
    visited_list = []
    stack = []

    route = turtle.Turtle()
    route.speed(0)
    # route.getscreen().tracer(10, 5)
    route.getscreen().tracer(0)
    wall = turtle.Turtle()
    # wall.getscreen().tracer(10, 5)
    wall.getscreen().tracer(0)
    wall.speed(0)
    route.pen(pencolor="lawngreen", pendown=False, fillcolor="lawngreen")
    wall.penup()
    # wall.right(90)
    wall.goto(center_starting_blocks[-1])
    # route.right(90)
    route.goto(center_starting_blocks[-1])
    route.pendown()

    # draw_square(cell_size, route, "green", "black")

    # Add the index of the center starting block pos in the list of all boxes to the visited list
    [visited_list.append(list_of_all_boxes_1d.index(pos))
     for pos in center_starting_blocks]

    # Add the index of the outline wall pos list pos in the list of all boxes to the visited list
    [visited_list.append(list_of_all_boxes_1d.index(pos))
     for pos in outline_wall_pos_list]
    [maze_wall_list.append(list_of_all_boxes_1d.index(pos))
     for pos in outline_wall_pos_list]

    # Add the index of the center starting block pos in the list of all boxes to the route list
    [maze_route.append(list_of_all_boxes_1d.index(pos))
     for pos in center_starting_blocks]

    # Add the index of the center starting block pos in the list of all boxes to the stack
    [stack.append(list_of_all_boxes_1d.index(pos))
     for pos in center_starting_blocks]

    current_index = list_of_all_boxes_1d.index(center_starting_blocks[0])

    while len(visited_list) < (len(list_of_all_boxes_1d)):

        random_index, wall_index = choose_random_move_index(
            current_index, horizontal_cells, vertical_cells, visited_list, stack)

        current_index = random_index
        current_wall_index = wall_index

        if current_index not in visited_list or current_index == None and current_wall_index not in visited_list or current_wall_index == None and current_index < len(list_of_all_boxes_1d):
            # check if the  there are no more places to go
            if len(stack) != 0:
                pass
            # Drawing the path
            if current_index != None and current_index < len(list_of_all_boxes_1d) and current_index not in visited_list:
                if current_index not in visited_list:
                    visited_list.append(current_index)
                if current_index not in stack:
                    stack.append(current_index)
                maze_route.append(current_index)
                route.penup()
                route.goto(list_of_all_boxes_1d[current_index])
                route.pendown()
                draw_square(cell_size, route, "lawngreen", "")

            # Drawing the walls
            if current_wall_index != None and current_wall_index < len(list_of_all_boxes_1d):
                visited_list.append(current_wall_index)

                maze_wall_list.append(current_wall_index)
                wall.goto(list_of_all_boxes_1d[current_wall_index])
                draw_square(cell_size, wall, "black", "")

    # open the exit points
    exits_list = open_exits(route, maze_route, maze_wall_list,
                            list_of_all_boxes_1d, horizontal_cells, vertical_cells)

    return exits_list, maze_route


def open_exits(route, maze_route, maze_wall_list, list_of_all_boxes_1d, horizontal_cells, vertical_cells):

    cells = horizontal_cells*vertical_cells
    exits_list = []
    # Open Top
    while True:
        random_top = random.randint(0, horizontal_cells)
        if random_top+horizontal_cells in maze_route:
            maze_route.append(random_top)
            maze_wall_list.remove(random_top)
            exits_list.append(random_top)
            route.penup()
            route.goto(list_of_all_boxes_1d[random_top])
            route.pendown()
            draw_square(cell_size, route, "lawngreen", "")
            break

    # Open bottom
    while True:
        random_bottom = random.randint((cells)-horizontal_cells, cells)
        if random_bottom-horizontal_cells in maze_route:
            maze_route.append(random_bottom)
            maze_wall_list.remove(random_bottom)
            exits_list.append(random_bottom)
            route.penup()
            route.goto(list_of_all_boxes_1d[random_bottom])
            route.pendown()
            draw_square(cell_size, route, "lawngreen", "")
            break

    # Open Left
    while True:
        # random_left = random.randint(0, cells)
        random_left = [num for num in range(
            0, cells) if num % horizontal_cells == 0]
        random_left = random.choice(random_left)
        if random_left+1 in maze_route:
            maze_route.append(random_left)
            maze_wall_list.remove(random_left)
            exits_list.append(random_left)
            route.penup()
            route.goto(list_of_all_boxes_1d[random_left])
            route.pendown()
            draw_square(cell_size, route, "lawngreen", "")
            break

    # Open Right
    while True:
        random_right = [
            num-1 for num in range(0, cells) if num % horizontal_cells == 0 and num > horizontal_cells]
        random_right = random.choice(random_right)
        if random_right-1 in maze_route:
            maze_route.append(random_right)
            maze_wall_list.remove(random_right)
            exits_list.append(random_right)
            route.penup()
            route.goto(list_of_all_boxes_1d[random_right])
            route.pendown()
            draw_square(cell_size, route, "lawngreen", "")
            break
    return exits_list


def convert_vec2d_to_int_tuple(vec2d_list: list) -> list:
    """Convert a vec2D list to a list of integers.

    Args:
        vec2d_list (list): a list containing tuples on vec2D values.

    Returns:
        list: a converted list.
    """

    for box in vec2d_list:
        index = vec2d_list.index(box)
        box_tuple = (int(box[0]), int(box[1]))
        if box_tuple[0] % cell_size != 0:
            if box_tuple[0] > 0:
                box_tuple = (box_tuple[0]+1, box_tuple[1])
            else:
                box_tuple = (box_tuple[0]-1, box_tuple[1])
        if box_tuple[1] % cell_size != 0:
            if box_tuple[1] > 0:
                box_tuple = (box_tuple[0], box_tuple[1]+1)
            else:
                box_tuple = (box_tuple[0], box_tuple[1]-1)

        vec2d_list[index] = (box_tuple)

    return vec2d_list

def draw_maze_solution():
    solver = turtle.Turtle()
    solver.penup()
    solver.goto(-(cell_size/2), cell_size/2)
    solver.pen(shown=True, pendown=True, pencolor="red", fillcolor="red")
    pass

def find_maze_route(exits_list, maze_route, list_of_all_boxes_1d, horizontal_cells, vertical_cells, target_exit):


    maze_route_pos = [list_of_all_boxes_1d[pos] for pos in maze_route]
    visited_list = []
    stack_list = []

    current_index = list_of_all_boxes_1d.index((0, 0))
    print("starting point: ", current_index)

    while len(visited_list) < len(maze_route) or current_index != target_exit:
        current_index, wall = choose_random_move_index(
            current_index, horizontal_cells, vertical_cells, visited_list, stack_list)

        if current_index not in visited_list or current_index != None and current_index < len(maze_route):
            # check if the index is in the list of visited indexes
            if current_index not in visited_list:
                visited_list.append(list_of_all_boxes_1d[current_index])

            # check if the index is in the stack list
            if current_index not in stack_list:
                stack_list.append(list_of_all_boxes_1d[current_index])

            pass
    
    return stack_list, maze_route_pos

def solve_maze(exits_list, maze_route, list_of_all_boxes_1d,
                   horizontal_cells, vertical_cells):
    target_exit = exits_list[0]
    print("Target exit: ", target_exit)
    list_of_paths = []
    for i in range(4):
        path, path_coordinates  = find_maze_route(exits_list, maze_route, list_of_all_boxes_1d,
                   horizontal_cells, vertical_cells, target_exit)
        list_of_paths.append(path)
    print()
    print("Iteration 1 list of paths: ")
    [print(f'{index}:', path) for index,path in enumerate(list_of_paths)]
    print()
    print(path_coordinates)
    
    # shortest_path = list_of_paths[0]
    # for path in list_of_paths:
    #     if len(path) < len(shortest_path):
    #         shortest_path = path
            
    # print("Iteration 1 list of paths: ")
    # [print(f'{index}:', path) for index,path in enumerate(list_of_paths)]
    
    # print()
    # print()
    # list_of_paths = []   
    # for j in range(4):
    #     path, path_coordinates  = find_maze_route(exits_list, shortest_path, list_of_all_boxes_1d,
    #                horizontal_cells, vertical_cells, target_exit)
    #     list_of_paths.append(path)    

    # print()
    # print("Iteration 2 list of paths: ")
    # [print(f'{index}:', path) for index,path in enumerate(list_of_paths)]
    # print()
    
    # shortest_path = list_of_paths[0]
    # for path in list_of_paths:
    #     if len(path) < len(shortest_path):
    #         shortest_path = path
    # print("Iteration 2 shortest path: ", len(shortest_path), shortest_path)
    pass

    pass


def run_maze():
    # global vertical_cells, horizontal_cells
    vertical_cells = int((-min_x + max_x) / cell_size)
    horizontal_cells = int((-min_y + max_y) / cell_size)
    screen = turtle.Screen()
    list_of_all_boxes_1d = fill_in_constraints_box(
        cell_size, min_x, max_y, vertical_cells, horizontal_cells)

    # print(list_of_all_boxes_1d)

    # list_of_all_boxes_1d = [((box[0]), int(box[1])) for box in list_of_all_boxes_1d]
    list_of_all_boxes_1d = convert_vec2d_to_int_tuple(list_of_all_boxes_1d)

    # print(list_of_all_boxes_1d)
    # print(len(list_of_all_boxes_1d))

    center_starting_blocks = draw_starting_point()
    screen.update()

    # center_starting_blocks = [(int(box[0]), int(box[0]) ) for box in center_starting_blocks]
    center_starting_blocks = convert_vec2d_to_int_tuple(center_starting_blocks)

    outline_wall_pos_list = draw_constraint_box(min_x, min_y, max_x, max_y)
    screen.update()

    # print("New List:", len(list_of_all_boxes_1d))

    exits_list, maze_route = create_maze_route(cell_size, min_x, min_y, max_x, max_y,
                                               list_of_all_boxes_1d, center_starting_blocks, outline_wall_pos_list)
    screen.update()
    
    solve_maze(exits_list, maze_route, list_of_all_boxes_1d,
                   horizontal_cells, vertical_cells)
    screen.update()

    screen.exitonclick()


if __name__ == "__main__":
    run_maze()
