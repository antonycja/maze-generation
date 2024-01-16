import unittest
from world.text import world as text
import sys



class WorldTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.position = {"x":0, "y":0}
        
    def test_position_allowed(self):
        output1 = text.is_position_allowed(0, self.position, 50, -100, -200, 100, 200)
        output2 = text.is_position_allowed(25, self.position, 90, -100, -200, 100, 200)
        self.assertTrue(output1)
        self.assertTrue(output2)
        
        
    def test_position_not_allowed(self):
        output1 = text.is_position_allowed(0, self.position, 500, -100, -200, 100, 200)
        output2 = text.is_position_allowed(25, self.position, 101, -100, -200, 100, 200)
        self.assertFalse(output1)
        self.assertFalse(output2)
        
    def test_text(self):
        import world.text.world 
        self.assertTrue('world' in sys.modules, "test_robot module should be found")
    
    # def test_turtle(self):
    #     import world.turtle.world 
    #     self.assertTrue('world' in sys.modules, "test_robot module should be found")
    #     pass