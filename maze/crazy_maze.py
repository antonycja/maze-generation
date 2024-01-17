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
    return turtle_name.get_poly()
    pass


def fill_in_constraints_box(cell_size, min_x, max_y, vertical_cells, horizontal_cells):
    list_of_blocks = []
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
            list_vertical_squares.append(list_of_squares)
            t.forward(cell_size)
            pass
        list_of_blocks.append(list_vertical_squares)
        t.right(90)
        t.forward(cell_size)
        t.left(90)
        t.back(vertical_cells*cell_size)
    t.getscreen().tracer(1)
    # [print(index, " -", box) for index, box in enumerate(list_of_blocks)]
    # print(len(list_of_blocks)*len(list_of_blocks[0]))
    # [print(block) for block in list_of_blocks]
    return list_of_blocks

    pass

def choose_random_move_index(current_index, cells):
    if current_index == 0:
        random_index = random.randint(current_index, current_index+1)
    elif current_index == cells-1:
        random_index = random.randint(current_index-1, current_index)
    else:
        random_index = random.randint(current_index-1, current_index+1)
        
    return random_index        
        
def is_maze_position_valid(position, visited_list):
    if position not in visited_list: # The position has not changed
        return True
    else:
        return False
        pass
    
    pass

def create_maze_route(cell_size, min_x, min_y, max_x, max_y, list_of_blocks):
    horizontal_cells = int((-min_x + max_x) / cell_size)
    vertical_cells = int((-min_y + max_y) / cell_size)
    maze_route = []
    maze_wall_list = []
    visited_list = []
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
    
    for line_of_blocks in list_of_blocks:
        current_line_index = list_of_blocks.index(line_of_blocks)
        random_y_index = choose_random_move_index(current_line_index, vertical_cells)

        for block in line_of_blocks:
            current_block_index = line_of_blocks.index(block)
            random_x_index = choose_random_move_index(current_block_index, horizontal_cells)
            
            """Start checking """
            
            if current_line_index != random_y_index:
                position = list_of_blocks[random_y_index][current_block_index]
                if is_maze_position_valid(position, visited_list):
                    visited_list.append(position)
                    stack.append(position)
                    print("From (Y): ", list_of_blocks[current_line_index][current_block_index])
                    print("To (Y): ", position)
                
                pass
                # 
            print("Random Y:", random_y_index)
            
            
            
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
    list_of_blocks = fill_in_constraints_box(
        cell_size, min_x, max_y, vertical_cells, horizontal_cells)
    create_maze_route(cell_size, min_x, min_y, max_x, max_y, list_of_blocks)

    screen.exitonclick()


if __name__ == "__main__":
    run_maze()
