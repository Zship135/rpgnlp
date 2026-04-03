import unittest
from rpgnlp import NLPEngine


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = NLPEngine()

    def test_case1(self):
        result = self.engine.run("go north", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "north")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")
    
    def test_case2(self):
        result = self.engine.run("go east", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "east")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case3(self):
        result = self.engine.run("go south", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "south")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case4(self):
        result = self.engine.run("go west", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "west")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case5(self):
        result = self.engine.run("go north east", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "north east")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")
    
    def test_case6(self):
        result = self.engine.run("go north west", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "north west")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case7(self):
        result = self.engine.run("go south east", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "south east")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case8(self):
        result = self.engine.run("go south west", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "south west")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case9(self):
        result = self.engine.run("go to the north gate", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "north gate")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case10(self):
        result = self.engine.run("go to the south east gate", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "south east gate")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case11(self):
        result = self.engine.run("go south east to the north west eastern gate", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "north west eastern gate")
        self.assertEqual(result["direction"], "south east")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case12(self):
        result = self.engine.run("talk to the old man", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "old man")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case13(self):
        result = self.engine.run("articulate complex matters to the old man.", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "old man")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")
    
    def test_case14(self):
        result = self.engine.run("slime the slime", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "slime")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case15(self):
        result = self.engine.run("run quickly north", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "north")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["quickly"])
        self.assertEqual(result["topic"], "")

    def test_case16(self):
        result = self.engine.run("smash the red door with the hammer", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "red door")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["hammer"])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case17(self):
        result = self.engine.run("look at the shiny sword", debug=True)
        self.assertEqual(result["action"], "inspect")
        self.assertEqual(result["subject"], "shiny sword")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case18(self):
        result = self.engine.run("go to the southern tower", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "southern tower")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case19(self):
        result = self.engine.run("speak to the wise old wizard", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "wise old wizard")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case20(self):
        result = self.engine.run("travel west with haste", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "west")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["haste"])
        self.assertEqual(result["topic"], "")

    def test_case21(self):
        result = self.engine.run("bash the goblin with haste", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "goblin")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["haste"])
        self.assertEqual(result["topic"], "")

    def test_case22(self):
        result = self.engine.run("bash the goblin with haste", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "goblin")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["haste"])
        self.assertEqual(result["topic"], "")

    def test_case23(self):
        result = self.engine.run("search for hidden doors", debug=True)
        self.assertEqual(result["action"], "search")
        self.assertEqual(result["subject"], "hidden doors")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case24(self):
        result = self.engine.run("tell the guard about the plan", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "guard")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "plan")
    
    def test_case25(self):
        result = self.engine.run("tell the guard about the plan with haste", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "guard")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["haste"])
        self.assertEqual(result["topic"], "plan")

    def test_case26(self):
        result = self.engine.run("hastily tell the guard about the plan", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "guard")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["hastily"])
        self.assertEqual(result["topic"], "plan")

    def test_case27(self):
        result = self.engine.run("tell the guard about the plan carefully", debug=True)
        self.assertEqual(result["action"], "speak")
        self.assertEqual(result["subject"], "guard")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["carefully"])
        self.assertEqual(result["topic"], "plan")

    def test_case28(self):
        result = self.engine.run("attack the orc with the sword furiously", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "orc")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["sword"])
        self.assertEqual(result["modifiers"], ["furiously"])
        self.assertEqual(result["topic"], "")

    def test_case29(self):
        result = self.engine.run("go north east to the ancient library", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "ancient library")
        self.assertEqual(result["direction"], "north east")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case30(self):
        result = self.engine.run("inspect the large heavy wooden chest", debug=True)
        self.assertEqual(result["action"], "inspect")
        self.assertEqual(result["subject"], "large heavy wooden chest")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case31(self):
        result = self.engine.run("run south with speed and stealth", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "south")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["speed", "stealth"])
        self.assertEqual(result["topic"], "")

    def test_case32(self):
        result = self.engine.run("smash the barricade with rage", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "barricade")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["rage"])
        self.assertEqual(result["topic"], "")

    def test_case33(self):
        result = self.engine.run("run with haste", debug=True)
        self.assertEqual(result["action"], "travel")
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], [])
        self.assertEqual(result["modifiers"], ["haste"])
        self.assertEqual(result["topic"], "")

    def test_case34(self):
        result = self.engine.run("attack the troll with a sword and a shield", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "troll")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["sword", "shield"])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case35(self):
        result = self.engine.run("smash the door with a hammer and rage", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "door")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["hammer"])
        self.assertEqual(result["modifiers"], ["rage"])
        self.assertEqual(result["topic"], "")

    def test_case36(self):
        result = self.engine.run("attack the dragon with the sword and the bow", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "dragon")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["sword", "bow"])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case37(self):
        result = self.engine.run("bash the gate with a mace and fury", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "gate")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["mace"])
        self.assertEqual(result["modifiers"], ["fury"])
        self.assertEqual(result["topic"], "")

    def test_case38(self):
        result = self.engine.run("attack the ogre with a sword, a shield, and a torch", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "ogre")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["sword", "shield", "torch"])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")

    def test_case39(self):
        result = self.engine.run("smash the door with rage and a hammer", debug=True)
        self.assertEqual(result["action"], "heavy_attack")
        self.assertEqual(result["subject"], "door")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["hammer"])
        self.assertEqual(result["modifiers"], ["rage"])
        self.assertEqual(result["topic"], "")

    def test_case40(self):
        result = self.engine.run("attack the orc with the heavy iron mace and the sharp dagger", debug=True)
        self.assertEqual(result["action"], "attack")
        self.assertEqual(result["subject"], "orc")
        self.assertEqual(result["direction"], "")
        self.assertEqual(result["instrument"], ["heavy iron mace", "sharp dagger"])
        self.assertEqual(result["modifiers"], [])
        self.assertEqual(result["topic"], "")



if __name__ == "__main__":
    unittest.main()
