
def draw_maze_solution(path_coordinates, target_exit, exits_list, cell_size, turtle):
    solver = turtle.Turtle(visible=False)
    solver.penup()
    solver.goto(-(cell_size/2), cell_size/2)
    solver.pendown()
    solver.pen(pencolor="blue", pensize=2, speed=10)
    for path in path_coordinates:
        if path != path_coordinates[-1]:
            solver.goto(path[0]+(cell_size/2), path[1]-(cell_size/2))
        else:
            if target_exit == exits_list[3]:
                solver.goto(path[0]+(cell_size), path[1]-(cell_size/2))
                
            elif target_exit == exits_list[2] :
                solver.goto(path[0], path[1]-(cell_size/2))
            elif target_exit == exits_list[1]:\
                solver.goto(path[0]+(cell_size/2), path[1]-cell_size)
            else:
                solver.goto(path[0]+(cell_size/2), path[1])


def find_maze_route(maze_route, list_of_all_boxes_1d, vertical_cells, horizontal_cells, target_exit, center_starting_pos, walls_list, choose_random_move_index, screen):

    # test = turtle.Turtle()
    # test.pencolor("red")
    visited_list = walls_list
    
    stack_list = []
    target_exit = list_of_all_boxes_1d.index(list_of_all_boxes_1d[target_exit])
    # maze_route.insert(0,(0,0))
    current_index = list_of_all_boxes_1d.index(center_starting_pos)
    # test.penup()
    # test.goto(list_of_all_boxes_1d[current_index])
    # test.pendown()
    # test.pensize(2)
    total_blocks = horizontal_cells*vertical_cells
    # print(total_blocks)
    # print("starting point: ", current_index)
    visited_list.append(current_index)
    if current_index not in stack_list:
        stack_list.append(current_index)
    while (len(visited_list)-len(walls_list)) != len(maze_route) or current_index != target_exit:
        
        if current_index == target_exit:
            break
       
        current_index, wall = choose_random_move_index(
            current_index, horizontal_cells, vertical_cells, visited_list, stack_list, total_blocks)
        
        if current_index == None:
            current_index = list_of_all_boxes_1d.index(center_starting_pos)
        
        if current_index > total_blocks:
            continue

        if (list_of_all_boxes_1d[current_index] in maze_route) and (list_of_all_boxes_1d.index(list_of_all_boxes_1d[current_index]) not in visited_list or current_index != None) and current_index < total_blocks:
            
            # print(current_index)
            
            # check if the index is in the list of visited indexes
            if list_of_all_boxes_1d.index(list_of_all_boxes_1d[current_index]) not in visited_list or list_of_all_boxes_1d[current_index] in maze_route:
                visited_list.append(list_of_all_boxes_1d.index(list_of_all_boxes_1d[current_index]))

                # test.goto(list_of_all_boxes_1d[current_index])
                screen.update()
            # check if the index is in the stack list
            # print(current_index)
            if current_index not in stack_list and list_of_all_boxes_1d[current_index] in maze_route:
                stack_list.append(list_of_all_boxes_1d.index(list_of_all_boxes_1d[current_index]))

            pass
        
    # print(stack_list)
        
    maze_route_pos = [list_of_all_boxes_1d[pos] for pos in stack_list]
    
    return stack_list, maze_route_pos


def solve_maze(target_exit, maze_route, list_of_all_boxes_1d,
                   horizontal_cells, vertical_cells, center_starting_pos, walls_list, choose_random_move_index, screen):
    
    maze_route = [list_of_all_boxes_1d[pos] for pos in maze_route]
    maze_route = [pos for pos in list_of_all_boxes_1d if pos in maze_route]
    
    # print("Target exit: ", target_exit)
    list_of_paths = []
    path, path_coordinates  = find_maze_route(maze_route, list_of_all_boxes_1d,
                horizontal_cells, vertical_cells, target_exit, center_starting_pos, walls_list, choose_random_move_index, screen)
    list_of_paths.append(path)

    # print(path_coordinates)
    return path_coordinates
    pass

