import random


def get_obstacles(min_x, min_y, max_x, max_y):
    num_of_obstacles = random.randint(0, 10)
    obstacle_pos_list = [tuple([random.randint(min_x, max_x), random.randint(
        min_y, max_y)]) for _ in range(num_of_obstacles)]
    # print(obstacle_pos_list)
    return obstacle_pos_list


def is_position_blocked(x_y_pos, obstacle_pos_list):
    # pos = (x, y)
    li = []
    for poses in obstacle_pos_list:
        for x_y in x_y_pos:
            if x_y[0] == poses[0] and x_y[1] == poses[1]:
                li.append(True)
            else:
                li.append(False)
    if True in li:
        return True
    else:
        return False


def is_path_blocked(formula, steps, x1, y1, obstacle_pos_list):
    x2, y2 = x1, y1
    if formula == 0:  # forward
        y2 = y1+int(steps)
    elif formula == 25:  # Turn Right
        x2 = x1+int(steps)
    elif formula == 5:  # Backwards
        y2 = y1 + int(steps)
    elif formula == 75:  # Turn left
        x2 = x1 + int(steps)

    if x1 != x2:
        x_y_pos = [(x, y1) for x in range(x1, x2+1)]
        if is_position_blocked(x_y_pos, obstacle_pos_list):
            # print(x, y)
            return True
        else:
            return False
    elif y1 != y2:
        x_y_pos = [(x1, y) for y in range(y1, y2+1)]
        if is_position_blocked(x_y_pos, obstacle_pos_list):
            # print(x, y)
            return True
        else:
            return False
    else:
        return False


def observations(obstacle_pos_list, robot_name):
    # print(f"{robot_name}: Loaded obstacles.")
    print("There are some obstacles:")
    [print(f"- At position {pos[0]},{pos[1]} (to {pos[0]+4},{pos[1]+4})")
     for pos in obstacle_pos_list]

