
def is_position_allowed(formula: int,position: dict, steps: int, min_x, min_y, max_x, max_y) -> bool:
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
    """Show the updated position of the robot on the terminal.

    Args:
        name (str): The name of the robot.
        direction (str): The current direction of the robot.
        steps (int, optional): The steps the robot must move by. Defaults to 0.

    Returns:
        str: The string containing the current move that was played.
    """
    if "forward" == direction.lower() or direction.lower() == "back":
        return (f" > {name} moved {direction} by {steps} steps.")
    else:
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
