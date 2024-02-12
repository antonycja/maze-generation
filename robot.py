from sys import argv
from maze.obstacles import *
from import_helper import dynamic_import
# from world.text.world import *
min_y, max_y = -200, 200
min_x, max_x = -100, 100
if len(argv) <= 2:
    maze_name = "obstacles"
    pass
if len(argv) == 2 and argv[1].lower() == "turtle":
    from world.turtle.world import *

elif len(argv) == 3:
    maze_name = argv[-1]
    maze = dynamic_import("maze." + maze_name)
    pass
    # setup_box(min_x, min_y, max_x, max_y)
else:
    from world.text.world import *
    maze_name = "obstacles"

# else:
#     from world.text.world import *


def get_robot_name() -> tuple:  # Returns the name of the robot
    """Gets the name of the robot from the user and greets the user.

    Returns:
        tuple(str, str): The name of the robot and the greeting message.
    """
    name = input("What do you want to name your robot? ")
    greet = f"{name}: Hello kiddo!"
    return name, greet


def get_action(robot_name: str, commands: dict, position: dict, direction: int, list_keys: list, movement_commands: list, movement_history: list, obstacles_list: list) -> str:
    """Get the next action for the robot to do, check if the command is valid and do the action. Retry until a valid command is given.

    Args:
        robot_name (str): The robot_name of the robot.
        commands (dict): The dictionary of the available commands.
        position (dict): The current position of the robot.
        direction (int): The direction of which the robot must go.
        list_keys (list): A list containing the commands 

    Returns:
        str: The valid action given by the user.
    """
    move_text, position_text, sprint_moves_list = "", "", []
    action = input(f"{robot_name}: What must I do next? ").strip()

    if action.lower() == "off":
        print(f"{robot_name}: Shutting down..")

    # Check if the command entered is help, if it is do the help and then ask again.
    elif action.lower() == "help":
        help_cmd(commands)
        get_action(robot_name, commands, position, direction,
                   list_keys, movement_commands, movement_history, obstacles_list)
    # Check if the command entered has the word replay if yes, do the replay and ask again.
    elif "replay" in action.lower().split():
        replay(robot_name, movement_history, position, direction,
               action, move_text, position_text, sprint_moves_list, obstacles_list)
        get_action(robot_name, commands, position, direction,
                   list_keys, movement_commands, movement_history, obstacles_list)

    # Check if the first command entered is not one of the valid commands that the robot understands from the list of commands then print out the error and ask again.
    elif action.split()[0].upper() not in list_keys:
        output(robot_name, f"Sorry, I did not understand '{action}'.")
        get_action(robot_name, commands, position, direction,
                   list_keys, movement_commands, movement_history, obstacles_list)

    elif "mazerun" in action.lower().split():
        print(f"> {robot_name} starting maze run..")
        if len(action.lower().split()) > 1:
            # TODO: solve a full maze
            
            if "top" in action.lower().split():
                print("I am at the top edge.")
            elif "right" in action.lower().split():
                print("I am at the right edge")
            elif "left" in action.lower().split():
                print("I am at the left edge")
            else:
                print("I am at the bottom edge")
            pass
        else:
            print("I am at the top edge.")
            pass
        get_action(robot_name, commands, position, direction,
                   list_keys, movement_commands, movement_history, obstacles_list)

    else:

        movement_history = record_history(
            movement_commands, action, movement_history)  # Record the history
        position, direction, move_text, position_text = move(
            action, robot_name, position, direction, move_text, position_text, sprint_moves_list, obstacles_list)
        if move_text:
            if isinstance(move_text, list):
                for text in move_text:
                    # Print each message text if the move text is a list.
                    output(message=text)
            else:
                output(message=move_text)  # Print the move text message.
        output(message=position_text)  # Print the position text message.
        get_action(robot_name, commands, position, direction,
                   list_keys, movement_commands, movement_history, obstacles_list)
    return action


def move_forward(steps: int, name: str, position: dict, direction: int, formula: int, obstacles_list: list) -> dict:
    """Move the robot forward (x) amount of steps making sure that the robot does not go over the safe zone and keeping track of its position after every move.

    Args:
        steps (int): The amount of steps the robot must move.
        name (str): The name of the robot.
        position (dict): The current position of the robot.
        direction (int): The current direction of the robot.

    Returns:
        dict: A dictionary containing the x and y coordinates of the position of the robot.
    """

    move_text = None
    if is_position_allowed(formula, position, steps, min_x, min_y, max_x, max_y):
        if is_path_blocked(formula, steps, position["x"], position["y"], obstacles_list):
            output(name, f"Sorry, there is an obstacle in the way.")
        else:
            update_position(formula, position, steps)
            move_text = show_move(name, "forward", steps)
    else:
        # Print the out of range message
        output(name, "Sorry, I cannot go outside my safe zone.")
    position_text = show_position(name, position)

    return position, move_text, position_text


def move_back(steps: int, name: str, position: dict, direction: dict, formula: int, obstacles_list: list) -> dict:
    """Move the robot back (x) amount of steps.

    Args:
        steps (int): The amount of steps to move by.
        name (str): The name of the robot.
        position (dict): The current position of the robot.
        direction (dict): The current direction of the robot.

    Returns:
        dict: A dictionary containing the x and y coordinates of the position of the robot. 
    """
    move_text = None
    if is_position_allowed(formula, position, -steps, min_x, min_y, max_x, max_y):
        if is_path_blocked(formula, steps, position["x"], position["y"], obstacles_list):
            output(name, " > Sorry, there is an obstacle in the way.")
        else:
            update_position(formula, position, -steps)
            move_text = show_move(name, "back", steps)
    else:
        output(name, "Sorry, I cannot go outside my safe zone.")

    position_text = show_position(name, position)
    return position, move_text, position_text


def sprint(steps: int, name: str, position: dict, direction: dict, sprint_moves_list: list, formula: int, obstacles_list: list) -> tuple:
    """Sprints the robot from the given number down to the 1.

    Args:
        steps (int): The steps the robot must move.
        name (str): The name of the robot.
        position (dict): The position of the robot.
        direction (dict): The direction of the robot.
        sprint_moves_list (list): The list of moves played in the sprints.

    Returns:
        tuple: a tuple consisting of (position, sprint_moves_list, position_text)
    """
    sprint_moves_list.append(show_move(name, "forward", steps))

    position['y'] += steps

    if steps < 2:  # Base case for the recursive function.
        position_text = show_position(name, position)
        return position, sprint_moves_list, position_text
    # Check if the position is allowed.
    if is_position_allowed(formula, position, steps, min_x, min_y, max_x, max_y) and steps >= 2:
        if is_path_blocked(position["x"], position["y"], position["x"]+steps, position["y"]+steps, obstacles_list):
            output(name, " > Sorry, there is an obstacle in the way.")
        else:
            return sprint(steps - 1, name, position, direction, sprint_moves_list, formula, obstacles_list)
    else:
        output(name, "Sorry, I cannot go outside my safe zone.")
        position_text = show_position(name, position)
    return position, sprint_moves_list, position_text


def turn_right(name: str, position: dict) -> dict:
    """Turn the robot to the right.

    Args:
        name (str): The name of the robot.
        position (dict): The current position of the robot.

    Returns:
        dict: A dictionary containing the x and y coordinates of the position of the robot.
    """
    move_text = show_move(name, "right")
    position_text = show_position(name, position)

    return position, move_text, position_text


def turn_left(name: str, position: dict) -> dict:
    """Turn the robot to the left.

    Args:
        name (str): The name of the robot.
        position (dict): The current position of the robot.

    Returns:
        dict: A dictionary containing the x and y coordinates of the position of the robot.
    """
    move_text = show_move(name, "left")
    position_text = show_position(name, position)

    return position, move_text, position_text


def help_cmd(commands: dict) -> None:
    """Takes in a dictionary of the available commands and their descriptions, formats and prints it out when the help function is called. 

    Args:
        commands (dict): The dictionary of commands.
    """
    output(message="I can understand these commands:")
    for key in commands:
        output(message=f"{key} - {commands[key]}")
    output(message="")


"""
Toy robot 3
"""


def record_history(movement_commands: list, command: str, movement_history: list) -> list:
    """Record every move that the robot makes.

    Args:
        movement_commands (list): The list of possible movement commands.
        command (str): The valid command entered.
        movement_history (list): The list containing the previous moves.

    Returns:
        list: The updated list if movements made by the robot.
    """
    if "replay" not in command and command .split()[0].lower() in movement_commands:
        movement_history.append(command)

    return movement_history


def replay(robot_name: str, movement_history: list, position: dict, direction: int, command: str, move_text: str, position_text: str, sprint_moves_list: list, obstacles_list: list) -> None:
    """Replay the commands that the robot previously played in different ways, such as in "reverse", "silent", etc.

    Args:
        robot_name (str): The name of the robot.
        movement_history (list): A list of all valid movements that the robot has made.
        position (dict): The position of the robot.
        direction (int): The direction of the robot.
        command (str): The valid command entered.
        move_text (str): The string for move text.
        position_text (str): The string for position text.
        sprint_moves_list (list): A list containing the sprint moves.
    """

    valid_replays = ["replay", "silent", "reversed"]
    replay_type = []
    command_list = command.lower().split()
    last_command_arg = command_list[-1].split("-")
    is_range_valid = [True if num.isdigit(
    ) else False for num in last_command_arg]
    is_valid = [
        True if command in valid_replays or command.isdigit() else False for command in command_list]

    if False in is_valid and False in is_range_valid:
        output(robot_name, f"Sorry, I did not understand '{command}'.")
    else:
        if command.lower().split()[0] == "replay":

            if "reversed" in command_list:
                movement_history = [movement_history[i]
                                    for i in range(len(movement_history)-1, -1, -1)]
                replay_type.append("in reverse")

            if len(command.split()) > 1 and command.split()[1].isdigit():
                movement_history = movement_history[int(command.split()[1])-1:]
                pass
            elif last_command_arg[0].isdigit() and last_command_arg[-1].isdigit():
                movement_history = movement_history[int(last_command_arg[-1])-1:int(
                    last_command_arg[0])+int(f"{-1 if len(last_command_arg) > 1 else +1}")]

            if "silent" in command_list:
                for movement in movement_history:
                    position, direction, move_text, position_text = move(
                        movement, robot_name, position, direction, move_text, position_text, sprint_moves_list, obstacles_list)
                replay_type.append("silently")

            else:
                for movement in movement_history:
                    position, direction, move_text, position_text = move(
                        movement, robot_name, position, direction, move_text, position_text, sprint_moves_list, obstacles_list)
                    output(message=move_text)
                    output(message=position_text)
            output(
                message=f" > {robot_name} replayed {len(movement_history)} commands{' '+' '.join(replay_type) if replay_type else ''}.")
        output(
            message=f" > {robot_name} now at position ({position['x']},{position['y']}).")


"""
Toy robot 3 end
"""


def move(action: str, name: str, position: dict, direction: dict, move_text, position_text, sprint_moves_list, obstacles_list) -> tuple:
    """Determines which move is correct to make. 

    Args:
        action (str): The command given by the user.
        name (str): The name of the robot.
        position (dict): The current position of the robot.
        direction (dict): The current direction of the robot.

    Returns:
        tuple: A tuple of dictionary, (position, direction, move_text, position_text)
    """
    steps = action.split()
    formula = int(str((direction+(3*360)) / 360).split(".")[1])
    if len(steps) == 2:
        steps = int(steps[1])
    else:
        steps = 0
    if "right" in action.lower():
        direction += 90
        position, move_text, position_text = turn_right(name, position)
    elif "left" in action.lower():
        direction -= 90
        position, move_text, position_text = turn_left(name, position)

    if "forward" in action.lower():
        position, move_text, position_text = move_forward(
            steps, name, position, direction, formula, obstacles_list)
    elif "sprint" in action.lower():
        position, move_text, position_text = sprint(
            steps, name, position, direction, sprint_moves_list, formula, obstacles_list)

    elif "back" in action.lower():
        position, move_text, position_text = move_back(
            steps, name, position, direction, formula, obstacles_list)

    return position, direction, move_text, position_text


def robot_start():
    """This is the entry function, do not change"""
    commands = {"OFF ": "Shut down robot",
                "HELP": "provide information about commands",
                "FORWARD (x)": "Moves the robot forward (x) steps",
                "BACK (x)": "Moves the robot backwards (x) steps",
                "RIGHT": "Turn the robot right(90 degrees)",
                "LEFT": "Turn the robot left(90 degrees)",
                "SPRINT (x)": "Make the robot sprint for the sum of all steps for x to 1",
                "REPLAY": "Filter out all non-movement commands and redo only the movement commands, providing the full output",
                "MAZERUN": "Find a way out of the maze."}

    movement_commands = ["forward", "back", "left", "right", "sprint"]
    # global obstacles_list
    position = {"x": 0, "y": 0}
    direction = 0
    list_keys = [key.split()[0] for key in commands.keys()]
    movement_history = []
    if maze_name != "obstacles":
        # Call the maze algo here
        #
        pass
    
    else:        
        try:
            obstacles_list = setup_box(min_x, min_y, max_x, max_y)
        except NameError:
            obstacles_list = get_obstacles(min_x, min_y, max_x, max_y)
        
    name, greet = get_robot_name()
    print(greet)
    print(f"{name}: Loaded {maze_name}.")
    if len(obstacles_list) > 0:
        observations(obstacles_list, name)
    get_action(name, commands, position, direction,
               list_keys, movement_commands, movement_history, obstacles_list)


if __name__ == "__main__":
    robot_start()
