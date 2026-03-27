import unittest
from rpgnlp import engine

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = engine.NLPEngine()

    def test_travel_north(self):
        result = self.engine.run("go north", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["direction"], "north")

    def test_travel_east(self):
        result = self.engine.run("go east", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["direction"], "east")

    def test_travel_south(self):
        result = self.engine.run("go south", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["direction"], "south")

    def test_travel_west(self):
        result = self.engine.run("go west", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["direction"], "west")
    
    def test_head_east(self):
        result = self.engine.run("head east", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["direction"], "east")

    def test_the_metal_rod(self):
        result = self.engine.run("Hit the goblin over the head with a metal rod", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "goblin")
        self.assertEqual(result["modifiers"], ["with"])
        self.assertEqual(result["instrument"], "metal rod")

    def test_case7(self):
        result = self.engine.run("Go inside of the house.", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "house")
        self.assertEqual(result["modifiers"], ["inside"])
    
if __name__ == "__main__":
    unittest.main()
