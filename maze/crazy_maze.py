import turtle
import random
from math import ceil

# min_x, min_y, max_x, max_y = random.choice([(
#     -100, -100, 100, 100), (-200, -100, 200, 100), (-100, -200, 100, 200), (-500, -300, 500, 300)])
min_x, min_y, max_x, max_y = -100, -200, 100, 200
print("box Size", (min_x, min_y, max_x, max_y))
# cell_size = random.choice([10, 20, 25,])
cell_size = random.choice([25])

# print("Cell size", cell_size)


def draw_constraint_box(min_x, min_y, max_x, max_y):
    tim = turtle.Turtle(visible=False)
    tim.getscreen().tracer(1)
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


def draw_starting_point():
    starting = turtle.Turtle(visible=True)
    starting.getscreen().tracer(1)
    center_starting_pos = []
    starting_y_point = cell_size
    for line in range(2):
        starting_x_point = cell_size*-1
        for row in range(2):
            starting.begin_poly()
            starting.goto(starting_x_point, starting_y_point)
            draw_square(cell_size, starting, "blue", "blue")
            starting_x_point += cell_size
            starting.end_poly()
            center_starting_pos.append(starting.get_poly())
        # Drawing down
        starting_y_point -= cell_size

    return center_starting_pos

    # starting.goto(starting_x_point, starting_y_point)
    # draw_square(cell_size, starting, "white", "black")


# TODO: Clean up this function by removing code that is not being used anymore and write comments

def fill_in_constraints_box(cell_size, min_x, max_y, vertical_cells, horizontal_cells):
    # list_of_blocks = []
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
        # list_vertical_squares = []
        for vertical in range(vertical_cells):
            list_of_squares = draw_square(cell_size, turtle_name=t)
            list_of_all_boxes_1d.append(list_of_squares)
            # list_vertical_squares.append(list_of_squares)
            t.forward(cell_size)
            pass
        # list_of_blocks.append(list_vertical_squares)
        t.right(90)
        t.forward(cell_size)
        t.left(90)
        t.back(vertical_cells*cell_size)
    # t.getscreen().tracer(1)

    # [list_of_all_boxes_1d.append(pos) for pos in center_starting_blocks]
    print(list_of_all_boxes_1d)
    print(len(list_of_all_boxes_1d))

    return list_of_all_boxes_1d

    pass


def choose_random_move_index(current_index, x_cells, y_cells, visited_list, stack, maze_route):
    # print(current_index + x_cells)
    len_of_obs = (x_cells*y_cells)
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
            if all(in_visited) and len(stack) != 1:
                # Do the stack reverse here

                # print("going back")
                stack.pop()
                random_index = stack[-1]
                wall_index = None
                break
            elif len(stack) == 1:
                # Check is the stack only have one value, if so then there are no more possible routes start placing walls where there isn't
                random_index = None
                for i in range(0, len_of_obs):
                    if i not in visited_list:
                        wall_index = i
                        break
                if wall_index:
                    break

    return random_index, wall_index


def is_maze_position_valid(position, visited_list):
    if position not in visited_list:  # The position has not changed
        return True
    else:
        return False
        pass

    pass


def create_maze_route(cell_size, min_x, min_y, max_x, max_y, list_of_all_boxes_1d, center_starting_blocks):
    horizontal_cells = int((-min_x + max_x) / cell_size)
    vertical_cells = int((-min_y + max_y) / cell_size)
    maze_route = [0]
    maze_wall_list = []
    visited_list = [0]
    stack = [0]

    route1 = turtle.Turtle()
    route2 = turtle.Turtle()
    route3 = turtle.Turtle()
    route4 = turtle.Turtle()

    wall1 = turtle.Turtle()
    wall2 = turtle.Turtle()
    wall3 = turtle.Turtle()
    wall4 = turtle.Turtle()

    route = turtle.Turtle()
    route.speed(0)
    route.getscreen().tracer(10, 5)
    wall = turtle.Turtle()
    wall.getscreen().tracer(10, 5)
    wall.speed(0)
    route.pen(pencolor="green", pendown=False, fillcolor="white")
    wall.penup()
    wall.goto(min_x, max_y)

    route.goto(min_x, max_y)
    route.pendown()

    draw_square(cell_size, route, "green", "black")
    [visited_list.append(pos) for pos in center_starting_blocks]
    [maze_route.append(pos) for pos in center_starting_blocks]

    current_index = 0

    while len(visited_list) < (len(list_of_all_boxes_1d)):

        random_index, wall_index = choose_random_move_index(
            current_index, horizontal_cells, vertical_cells, visited_list, stack, maze_route)

        current_index = random_index
        current_wall_index = wall_index

        if current_index not in visited_list or current_index == None and current_wall_index not in visited_list or current_wall_index == None and current_index < len(list_of_all_boxes_1d):
            # check if the  there are no more places to go
            if len(stack) != 0:
                pass
            # Drawing the path
            if current_index != None and current_index < len(list_of_all_boxes_1d):
                if current_index not in visited_list:
                    visited_list.append(current_index)
                if current_index not in stack:
                    stack.append(current_index)
                maze_route.append(current_index)
                route.goto(list_of_all_boxes_1d[current_index][0])
                draw_square(cell_size, route, "green", "black")

            # Drawing the walls
            if current_wall_index != None and current_wall_index < len(list_of_all_boxes_1d):
                visited_list.append(current_wall_index)

                maze_wall_list.append(current_wall_index)
                wall.goto(list_of_all_boxes_1d[current_wall_index][0])
                draw_square(cell_size, wall, "red", "black")

    # draw_starting_point()
    # route1.home()

    # print("Wall List: ", maze_wall_list)
    # print()
    # print("Path List: ", maze_route)
    # print()
    # print("Visited List: ", sorted(visited_list))


def check_right():
    pass


def run_maze():
    vertical_cells = int((-min_x + max_x) / cell_size)
    horizontal_cells = int((-min_y + max_y) / cell_size)
    screen = turtle.Screen()
    draw_constraint_box(min_x, min_y, max_x, max_y)
    list_of_all_boxes_1d = fill_in_constraints_box(
        cell_size, min_x, max_y, vertical_cells, horizontal_cells)

    center_starting_blocks = draw_starting_point()
    for pos in center_starting_blocks:
        for curr_pos in list_of_all_boxes_1d:
            if pos == curr_pos:
                list_of_all_boxes_1d.remove(curr_pos)
    
    create_maze_route(cell_size, min_x, min_y, max_x, max_y,
                      list_of_all_boxes_1d, center_starting_blocks)

    screen.exitonclick()


if __name__ == "__main__":
    run_maze()
