import turtle
from maze.obstacles import get_obstacles, is_path_blocked
screen = turtle.Screen()
screen.bgcolor("#000000")
hal = turtle.Turtle(shape="turtle")
hal.left(90)
hal.pen(fillcolor="red", pencolor="green", pensize=1, speed=2, pendown=True)


def draw_box(min_x, min_y, max_x, max_y) -> None:
    """Draw the canvas with turtle of the robot using the maximum and the minimum x and y coordinates. 
    The robot will only be able to move within this box.
    """
    box = turtle.Turtle(visible=False)
    box.pen(pencolor="yellow", pensize=5, speed=4, pendown=False)
    box.goto(min_x+8, min_y+8)
    box.pendown()
    for _ in range(2):
        box.forward(max_x - min_x + 3)
        box.left(90)
        box.forward(max_y - min_y + 3)
        box.left(90)


def draw_obstacles(min_x, min_y, max_x, max_y):
    print("Drawing obstacles")
    obstacles_list = get_obstacles(min_x, min_y, max_x, max_y)
    for pos in obstacles_list:
        square = turtle.Turtle(visible=False)
        square.pen(speed=0, pendown=False, pensize=0,
                   pencolor="green", fillcolor="green")
        square.goto(pos[0], pos[1])
        square.pendown()
        square.begin_fill()
        for _ in range(4):
            square.forward(8)
            square.left(90)
        square.end_fill()
    return obstacles_list


def setup_box(min_x, min_y, max_x, max_y):
    draw_box(min_x, min_y, max_x, max_y)
    obstacles_list = draw_obstacles(min_x, min_y, max_x, max_y)
    return obstacles_list


def is_position_allowed(formula, position: dict, steps: int, min_x, min_y, max_x, max_y) -> bool:
    """check whether the position that the robot is about to move to is valid or not 
    by checking if the new position will be in or outside the box.

    Args:
        position (dict): The current position of the robot before is moves to the new position.
        steps (int): The steps that the robot must move.

    Returns:
        bool: is_valid is a boolean that determines whether the position is valid or not.
    """

    pos_x, pos_y = position['x'], position['y']
    if formula == 0:
        pos_y += int(steps)
    elif formula == 5:
        pos_y -= int(steps)
    elif formula == 25:
        pos_x += int(steps)
    else:
        pos_x -= int(steps)

    is_valid = min_x <= pos_x <= max_x and min_y <= pos_y <= max_y
    return is_valid


def update_position(formula: int, position: dict, steps: int) -> None:
    """Update the position of the robot to the new valid position.

    Args:
        formula (int): The formula used to check the direction of the robot.
        position (dict): The current position to be updated.
        steps (int): The amount of steps the robot needs to move.
    """
    if formula == 0:  # forward
        position['y'] += int(steps)
    elif formula == 25:  # Turn Right
        position['x'] += int(steps)
    elif formula == 5:  # Backwards
        position['y'] -= int(steps)
    elif formula == 75:  # Turn left
        position['x'] -= int(steps)


def show_move(name: str, direction: str, steps: int = 0) -> str:
    """Move and turn the robot(turtle) to it new position whilst drawing a line 
    on the graphical user interface and then return the movement string.

    Args:
        name (str): The name of the robot.
        direction (str): The current direction of the robot.
        steps (int, optional): The steps the robot must move by. Defaults to 0.

    Returns:
        str: The string containing the current move that was played.
    """
    if "forward" == direction.lower() or direction.lower() == "back":
        # Move the turtle forward or backwards depending the direction.
        f'{hal.forward(steps) if direction == "forward" else hal.back(steps)}'
        return (f" > {name} moved {direction} by {steps} steps.")
    else:
        # Turn the turtle right or left depending the direction.
        f'{hal.right(90) if direction == "right" else hal.left(90)}'
        return (f" > {name} turned {direction}.")


def show_position(name: str, position: dict) -> str:
    """Show the updated position of the robot.

    Args:
        name (str): The name of the robot.
        position (dict): The new current updated position of the robot.

    Returns:
        str: The string stating the new position of the robot.
    """
    return (f" > {name} now at position ({position['x']},{position['y']}).")


def output(name: str = "", message: str = ""):
    """Print the output message.

    Args:
        name (str, optional): The name of the robot. Defaults to "".
        message (str, optional): The message to be printed. Defaults to "".
    """
    print(f"{f'{name}: ' if name else ''}{message}")


# screen.exitonclick()
