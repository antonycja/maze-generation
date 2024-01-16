import unittest
from test_base import captured_io, captured_output
from maze import obstacles

class WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.obstacle_pos_list_y_invalid = [(0,4), (0,21)]
        self.obstacle_pos_list = [(48, -19), (-32, 151), (-88, 173), (-22, 84), (-17, -57), (81, -143), (54, 181), (7, 196), (-44, -186), (100, 89)]
        self.x_y_pos = [(0,y) for y in range(10)]
        self.formula = int(str((0+(3*360)) / 360).split(".")[1])
        
    def test_position_blocked(self):
        output = obstacles.is_position_blocked(self.x_y_pos, self.obstacle_pos_list_y_invalid)
        self.assertTrue(output)
        pass
    
    def test_position_not_blocked(self):
        output = obstacles.is_position_blocked(self.x_y_pos, self.obstacle_pos_list)
        self.assertFalse(output)
        pass
    
    def test_get_obstacles(self):
        output = obstacles.get_obstacles(-100, -200, 100, 200)
        if len(output) > 0:
            list_item = output[-1]
            self.assertIsInstance(list_item, tuple)
            self.assertEqual(len(list_item), 2)
        self.assertIsInstance(output, list)
        
    def test_path_blocked(self):
        output = obstacles.is_path_blocked(0, 100, 100, 50, self.obstacle_pos_list)
        self.assertTrue(output)
        
    def test_path_not_blocked(self):
        output = obstacles.is_path_blocked(5, 100, 0, 0, self.obstacle_pos_list)
        self.assertFalse(output)
        