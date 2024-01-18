import turtle
import random

# min_x, min_y, max_x, max_y = random.choice([(
#     -100, -100, 100, 100), (-200, -100, 200, 100), (-100, -200, 100, 200)])
min_x, min_y, max_x, max_y = -100, -100, 100, 100
# print("box Size", (min_x, min_y, max_x, max_y))
# cell_size = random.choice([10, 20, 25,])
cell_size = random.choice([50])

# print("Cell size", cell_size)


def draw_constraint_box(min_x, min_y, max_x, max_y):
    tim = turtle.Turtle(visible=False)
    tim.pen(speed=0, pendown=False)
    tim.goto(min_x, max_y)
    tim.pendown()

    tim.goto(max_x, max_y)
    tim.right(90)
    tim.goto(max_x, min_y)
    tim.right(90)
    tim.goto(min_x, min_y)
    tim.right(90)
    tim.goto(min_x, max_y)

    pass


def draw_square(cell_size, turtle_name, color="black", pen_color="red"):
    turtle_name.begin_poly()
    turtle_name.pencolor(pen_color)
    turtle_name.fillcolor(color)
    turtle_name.pen(shown=True, pencolor=pen_color, fillcolor=color, speed=1)
    turtle_name.begin_fill()
    for _ in range(4):
        turtle_name.forward(cell_size)
        turtle_name.right(90)
    turtle_name.end_fill()
    turtle_name.end_poly()
    turtle_name.penup()
    return turtle_name.get_poly()
    pass


def fill_in_constraints_box(cell_size, min_x, max_y, vertical_cells, horizontal_cells):
    list_of_blocks = []
    list_of_all_boxes_1d = []
    print("Vertical", vertical_cells)
    print("Horizontal", horizontal_cells)
    t = turtle.Turtle()
    t.speed(1)
    t.getscreen().tracer(0)
    t.penup()
    t.goto(min_x, max_y)
    t.pendown()

    for horizontal in range(horizontal_cells):
        list_vertical_squares = []
        for vertical in range(vertical_cells):
            list_of_squares = draw_square(cell_size, turtle_name=t)
            list_of_all_boxes_1d.append(list_of_squares)
            list_vertical_squares.append(list_of_squares)
            t.forward(cell_size)
            pass
        list_of_blocks.append(list_vertical_squares)
        t.right(90)
        t.forward(cell_size)
        t.left(90)
        t.back(vertical_cells*cell_size)
    t.getscreen().tracer(1)

    print(list_of_all_boxes_1d)
    print(len(list_of_all_boxes_1d))
    # [print(index, " -", box) for index, box in enumerate(list_of_blocks)]
    # print(len(list_of_blocks)*len(list_of_blocks[0]))
    # [print(block) for block in list_of_blocks]
    return list_of_blocks, list_of_all_boxes_1d

    pass


def choose_random_move_index(current_index, x_cells, y_cells, visited_list):
    # print(current_index + x_cells)
    len_of_obs = (x_cells*y_cells)

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

    while True:
        random_index = random.choice(list_of_directions)
        if random_index not in visited_list:
            list_of_directions.remove(random_index)
            while True:
                wall_index = random.choice(list_of_directions)
                if wall_index not in visited_list:
                    break
                list_of_directions.remove(wall_index)
                if len(list_of_directions) == 0:
                    wall_index = None
                    break

            # indexes.append(random_index)
            # indexes.append(wall_index)
            break
        else:
            pass

    return random_index, wall_index


def is_maze_position_valid(position, visited_list):
    if position not in visited_list:  # The position has not changed
        return True
    else:
        return False
        pass

    pass


def create_maze_route(cell_size, min_x, min_y, max_x, max_y, list_of_blocks, list_of_all_boxes_1d):
    horizontal_cells = int((-min_x + max_x) / cell_size)
    vertical_cells = int((-min_y + max_y) / cell_size)
    maze_route = [0]
    maze_wall_list = []
    visited_list = [0]
    stack = []

    route = turtle.Turtle()
    route.speed(1)

    wall = turtle.Turtle()
    wall.speed(1)
    route.pen(pencolor="green", pendown=False, fillcolor="white")
    wall.penup()
    wall.goto(min_x, max_y)

    route.goto(min_x, max_y)
    route.pendown()

    draw_square(cell_size, route, "green", "black")

    current_index = 0

    while len(visited_list) < (len(list_of_all_boxes_1d)):

        random_index, wall_index = choose_random_move_index(
            current_index, horizontal_cells, vertical_cells, visited_list)

        # if random_index == len(list_of_all_boxes_1d):
        #     current_index == random_index-1
        # else: current_index = random_index
        # if wall_index == len(list_of_all_boxes_1d):
        #     current_wall_index = wall_index-1
        # else:
        # current_wall_index = wall_index

        current_index = random_index
        current_wall_index = wall_index

        if current_index not in visited_list and current_wall_index not in visited_list or current_wall_index == None and current_index < len(list_of_all_boxes_1d):
            if current_index != None and current_index < len(list_of_all_boxes_1d):
                visited_list.append(current_index)
                maze_route.append(current_index)
                route.goto(list_of_all_boxes_1d[current_index][0])
                draw_square(cell_size, route, "green", "black")
            if current_wall_index != None and current_wall_index < len(list_of_all_boxes_1d):
                visited_list.append(current_wall_index)
                maze_wall_list.append(current_wall_index)
                wall.goto(list_of_all_boxes_1d[current_wall_index][0])
                draw_square(cell_size, wall, "red", "black")

    print("Wall List: ", maze_wall_list)
    print()
    print("Path List: ", maze_route)
    print()
    print("Visited List: ", sorted(visited_list))

    # if current_index == len(list_of_all_boxes_1d):
    #     break

    # for line_of_blocks in list_of_blocks:
    #     current_line_index = list_of_blocks.index(line_of_blocks)
    #     """Get a random line index and Check to make sure that the position is valid."""
    #     if current_line_index == 0:
    #         rand_line = random.randint(
    #             current_line_index, current_line_index+1)
    #         if rand_line == current_line_index:
    #             wall_line = current_line_index+1
    #         else:
    #             wall_line = current_line_index
    #     elif current_line_index == (vertical_cells-1):
    #         rand_line = random.randint(
    #             current_line_index-1, current_line_index)
    #         if rand_line == current_line_index:
    #             wall_line = current_line_index-1
    #         else:
    #             wall_line = current_line_index
    #     else:
    #         rand_line = random.randint(
    #             current_line_index-1, current_line_index+1)
    #         # FIXED: LOGIC NEEDS to be fixed
    #         if rand_line == current_line_index-1:
    #             # TODO: Add an if statement to check if the block hasn't been used already.
    #             if current_line_index+1 in visited_list:
    #                 wall_line = current_line_index+1
    #             else:
    #                 wall_line = current_line_index

    #         elif rand_line == current_line_index+1:
    #             if current_line_index-1 in visited_list:
    #                 wall_line = current_line_index-1
    #             else:
    #                 wall_line = current_line_index
    #         else:
    #             wall_line = current_line_index

    #     # print(rand_line)

    #     for block in line_of_blocks:
    #         current_block_index = line_of_blocks.index(block)

    #         """Generate random block index and Check to make sure that the position is valid."""
    #         if current_block_index == 0:
    #             rand_block = random.randint(
    #                 current_block_index, current_block_index+1)
    #             if rand_block == current_block_index:
    #                 wall_line = current_block_index+1
    #             else:
    #                 wall_line = current_block_index
    #         elif current_block_index == horizontal_cells-1:
    #             rand_block = random.randint(
    #                 current_block_index-1, current_block_index)
    #             if rand_block == current_block_index:
    #                 wall_line = current_block_index-1
    #             else:
    #                 wall_line = current_block_index
    #         else:
    #             rand_block = random.randint(
    #                 current_block_index-1, current_block_index+1)
    #             if rand_line == current_block_index-1:
    #             # TODO: Add an if statement to check if the block hasn't been used already.
    #                 if current_block_index+1 in visited_list:
    #                     wall_line = current_block_index+1
    #                 else:
    #                     wall_line = current_block_index

    #             elif rand_line == current_block_index+1:
    #                 if current_block_index-1 in visited_list:
    #                     wall_line = current_block_index-1
    #                 else:
    #                     wall_line = current_block_index
    #             else:
    #                 wall_line = current_block_index

    #         if current_line_index != rand_line:
    #             """Move the Y(line) axis only"""
    #             print("Moving The Line")
    #             path_pos = list_of_blocks[rand_line][current_block_index]
    #             obs_pos = list_of_blocks[wall_line][current_block_index]
    #         else:
    #             """Move the block in the (X) axis"""
    #             print("Moving The Block")
    #             path_pos = list_of_blocks[current_line_index][rand_block]
    #             obs_pos = list_of_blocks[wall_line][rand_block]

    #         if path_pos not in visited_list and path_pos not in maze_wall_list:
    #             route.penup()
    #             route.goto(path_pos[0])
    #             route.pendown()
    #             draw_square(cell_size, route, "white", "black")
    #             if obs_pos in visited_list or obs_pos in maze_wall_list:
    #                 continue
    #             else:
    #                 wall.goto(obs_pos[0])
    #                 wall.pendown()
    #                 draw_square(cell_size, wall, "blue", "red")
    #                 wall.penup()
    #                 maze_wall_list.append(obs_pos)
    #                 visited_list.append(obs_pos)
    #                 print("Drawing Wall")

    #             print("Drawing Path")
    #             visited_list.append(path_pos)

    #             # list_of_blocks[rand_line].pop(current_block_index)
    #         else:
    #             print("Already Used")
    #             continue


def check_right():
    pass


def run_maze():
    vertical_cells = int((-min_x + max_x) / cell_size)
    horizontal_cells = int((-min_y + max_y) / cell_size)
    screen = turtle.Screen()
    draw_constraint_box(min_x, min_y, max_x, max_y)
    list_of_blocks, list_of_all_boxes_1d = fill_in_constraints_box(
        cell_size, min_x, max_y, vertical_cells, horizontal_cells)
    create_maze_route(cell_size, min_x, min_y, max_x, max_y,
                      list_of_blocks, list_of_all_boxes_1d)

    screen.exitonclick()


if __name__ == "__main__":
    run_maze()
