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

if __name__ == "__main__":
    unittest.main()
