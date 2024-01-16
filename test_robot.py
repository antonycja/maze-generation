import unittest
import robot
from unittest.mock import patch
from test_base import captured_io, captured_output
from io import StringIO
import random
import sys


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # direction = robot.robot_start
        self.robot_name = ["Tim", "tom"]
        self.move_forward = "FoRwarD 10"
        self.commands = {"OFF ": "Shut down robot",
                         "HELP": "provide information about commands",
                         "FORWARD (x)": "Moves the robot forward (x) steps",
                         "BACK (x)": "Moves the robot backwards (x) steps",
                         "RIGHT": "Turn the robot right(90 degrees)",
                         "LEFT": "Turn the robot left(90 degrees)",
                         "SPRINT (x)": "Make the robot sprint for the sum of all steps for x to 1"}
        self.keys = [key.split()[0] for key in self.commands.keys()]
        self.position = {"x": 0, "y": 0}
        self.movement_commands = ("forward", "back", "left", "right", "sprint")
        self.movement_history = []
        self.obstacles_list = [(48, -19), (-32, 151), (-88, 173), (-22, 84), (-17, -57), (81, -143), (54, 181), (7, 196), (-44, -186), (100, 89)]

        
        # self.formula = int(str((direction+(3*360)) / 360).split(".")[1])
        pass

    def test_robot_name_and_greet(self):
        with captured_io(StringIO(f"Tim\ntom")) as (out, err):
            name, greet = robot.get_robot_name()
        expected_name = self.robot_name
        expected_greet = f"{name}: Hello kiddo!"

        self.assertIn(name, expected_name)
        self.assertEqual(expected_greet, greet)

    def test_invalid_cmd(self):
        with captured_io(StringIO("Jump\noff\n")) as (out, err):
            robot.get_action(
                self.robot_name[0], self.commands, self.position, 0,  self.keys, self.movement_commands, self.movement_history, self.obstacles_list)

        output = out.getvalue().strip("\n")
        expected_action = f"""{self.robot_name[0]}: What must I do next? {self.robot_name[0]}: Sorry, I did not understand 'Jump'.
Tim: What must I do next? Tim: Shutting down.."""
        self.assertEqual(expected_action, output)
        pass
        # self.assertIn(robot.get_action(self.robot_name), self.commands)

    def test_valid_cmd(self):
        with captured_io(StringIO(f"{self.move_forward}\noff\n")) as (out, err):
            action = robot.get_action(
                self.robot_name[0], self.commands, self.position, 0, self.keys, self.movement_commands, self.movement_history, self.obstacles_list)

        self.assertEqual(action.lower(), "forward 10")

    def test_move_forward(self):
        with captured_io(StringIO(f"{self.move_forward}\n")) as (out, err):
            move = self.move_forward.split()
            position = robot.move_forward(move[1], self.robot_name[0], self.position, direction = 0, formula=0, obstacles_list=self.obstacles_list)
        self.assertEqual(position[0], {"y": 10, "x": 0})
        self.assertIn(move[0].upper(), self.keys)
        
    def test_move_back(self):
        move_back = "back 10"
        with captured_io(StringIO(f"{move_back}\n")) as (out, err):
            move = move_back.split()
            position = robot.move_back(int(move[1]), self.robot_name[0], self.position, direction=0, formula=0, obstacles_list=self.obstacles_list)
        self.assertEqual(position[0], {"y": -10, "x": 0})
        self.assertIn(move[0].upper(), self.keys)
        
        
    def test_turn_right(self):
        right = "right"
        with captured_io(StringIO(f"{right}\n{self.move_forward}")) as (out, err):
            move = right.split()
            move_f = self.move_forward.split()
            position = robot.turn_right(self.robot_name[0], self.position)
            position = robot.move_forward(move_f[1], self.robot_name[0], self.position, 90, 25, self.obstacles_list)
            
        self.assertEqual(position[0], {"y": 0, "x": 10})
        self.assertIn(move[0].upper(), self.keys)
    
    def test_turn_left(self):
        left = "left"
        with captured_io(StringIO(f"{left}\n{self.move_forward}")) as (out, err):
            move = left.split()
            move_f = self.move_forward.split()
            position = robot.turn_left(self.robot_name[0], self.position)
            position = robot.move_forward(int(move_f[1]), self.robot_name[0], self.position, direction=-90, formula=75, obstacles_list=self.obstacles_list)
            
        self.assertEqual(position[0], {"y": 0, "x": -10})
        self.assertIn(move[0].upper(), self.keys)
    
    def test_move_straight_limit(self):
        with captured_io(StringIO(f"forward 300\n")) as (out, err):
            position = robot.move_forward(30, self.robot_name[0], self.position, direction=0, formula=0, obstacles_list=self.obstacles_list)
            position = robot.move_forward(300, self.robot_name[0], self.position, direction=0, formula=0, obstacles_list=self.obstacles_list)
        output = out.getvalue().strip("\n")
        expected_output = f"""{self.robot_name[0]}: Sorry, I cannot go outside my safe zone."""
        self.assertIn(expected_output, output)
        self.assertEqual(position[0], {"y": 30, "x": 0})
        
    def test_move_turn_limit(self):
        with captured_io(StringIO(f"forward 100\n")) as (out, err): 
            position = robot.move_forward(30, self.robot_name[0], self.position, direction=90, formula=25, obstacles_list=self.obstacles_list)
            position = robot.move_forward(300, self.robot_name[0], self.position, direction=0, formula=0, obstacles_list=self.obstacles_list)
        output = out.getvalue().strip("\n")
        expected_output = f"""{self.robot_name[0]}: Sorry, I cannot go outside my safe zone."""
        self.assertIn(expected_output, output)
        self.assertEqual(position[0], {"y": 0, "x": 30})

    def test_unittest_exist(self):
        import test_robot 
        self.assertTrue('test_robot' in sys.modules, "test_robot module should be found")


if __name__ == "__main__":
    unittest.main()