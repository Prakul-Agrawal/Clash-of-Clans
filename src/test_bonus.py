import unittest, sys, os
import king, village, points as pt, buildings as bd

class TestKingAttackTarget(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """initialize the village and king"""
        self.V = village.createVillage(3)
        self.King = king.getHero(0)


    def setUp(self):
        """make sure the king is alive and new townhall is created before each unit test"""
        self.King.alive = True
        self.V.town_hall_obj = bd.TownHall((6,16), self.V)
        self.V.cannon_objs[(0,15)] = bd.Cannon((0,15), self.V)
        self.V.hut_objs[(5,0)] = bd.Hut((5,0), self.V)
        self.V.wizard_tower_objs[(17,27)] = bd.WizardTower((17,27), self.V)
        self.V.wall_objs[(0,35)] = bd.Wall((0,35), self.V)

    
    def test_building_destruction(self):
        """ensure correct behaviour when buildings are destroyed"""
        for target in (self.V.cannon_objs[(0,15)], self.V.hut_objs[(5,0)], self.V.wizard_tower_objs[(17,27)],
                       self.V.town_hall_obj, self.V.wall_objs[(0,35)]):
            self.assertEqual(self.King.attack_target(target, 2), None, "Return Value not None")
            self.assertFalse(target.destroyed, "Target destroyed at wrong health")

            self.assertEqual(self.King.attack_target(target, target.max_health - 3), None, "Return Value not None")
            self.assertFalse(target.destroyed, "Target destroyed at wrong health")

        target = self.V.cannon_objs[(0,15)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")

        target = self.V.hut_objs[(5,0)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")

        target = self.V.wizard_tower_objs[(17,27)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")

        target = self.V.wall_objs[(0,35)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")

        target = self.V.town_hall_obj
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")
        self.assertEqual(self.V.town_hall_obj, None, "Not None")
        coords = target.position
        for i in range(coords[0], coords[0]+4):
            for j in range(coords[1], coords[1]+3):
                self.assertEqual(self.V.map[i][j], pt.BLANK, "Map not updated")

        target = self.V.cannon_objs[(10,22)]
        length = len(self.V.cannon_objs)
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")
        self.assertEqual(length-1, len(self.V.cannon_objs), "Wrong dictionary length")
        self.assertNotIn((10,22),self.V.cannon_objs, "Building not removed from dictionary")
        coords = target.position
        for i in range(coords[0], coords[0]+2):
            for j in range(coords[1], coords[1]+2):
                self.assertEqual(self.V.map[i][j], pt.BLANK, "Map not updated")

        target = self.V.hut_objs[(6,11)]
        length = len(self.V.hut_objs)
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")
        self.assertEqual(length-1, len(self.V.hut_objs), "Wrong dictionary length")
        self.assertNotIn((6,11),self.V.hut_objs, "Building not removed from dictionary")
        coords = target.position
        for i in range(coords[0], coords[0]+2):
            for j in range(coords[1], coords[1]+2):
                self.assertEqual(self.V.map[i][j], pt.BLANK, "Map not updated")

        target = self.V.wizard_tower_objs[(7,27)]
        length = len(self.V.wizard_tower_objs)
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")
        self.assertEqual(length-1, len(self.V.wizard_tower_objs), "Wrong dictionary length")
        self.assertNotIn((17,27),self.V.wizard_tower_objs, "Building not removed from dictionary")
        coords = target.position
        self.assertEqual(self.V.map[coords[0]][coords[1]], pt.BLANK, "Map not updated")

        target = self.V.wall_objs[(3,10)]
        length = len(self.V.wall_objs)
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertTrue(target.destroyed, "Target not destroyed at 0 health")
        self.assertEqual(length-1, len(self.V.wall_objs), "Wrong dictionary length")
        self.assertNotIn((3,10),self.V.wall_objs, "Building not removed from dictionary")
        coords = target.position
        self.assertEqual(self.V.map[coords[0]][coords[1]], pt.BLANK, "Map not updated")

    
    
    def test_health_reduced(self):
        """ensure that target health is reduced by correct amount"""
        for target in (self.V.cannon_objs[(0,15)], self.V.hut_objs[(5,0)], self.V.wizard_tower_objs[(17,27)],
                       self.V.town_hall_obj, self.V.wall_objs[(0,35)]):
            init_health = target.health
            self.assertEqual(self.King.attack_target(target, 2), None, "Return Value not None")
            self.assertEqual(init_health - 2, target.health, "Health not correct")

            self.assertEqual(self.King.attack_target(target, target.max_health - 3), None, "Return Value not None")
            self.assertEqual(1, target.health, "Health not correct")

        target = self.V.cannon_objs[(0,15)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.hut_objs[(5,0)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.wizard_tower_objs[(17,27)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.wall_objs[(0,35)]
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.town_hall_obj
        self.assertEqual(self.King.attack_target(target, 1), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        self.V.town_hall_obj = bd.TownHall((6,16), self.V)
        self.V.cannon_objs[(0,15)] = bd.Cannon((0,15), self.V)
        self.V.hut_objs[(5,0)] = bd.Hut((5,0), self.V)
        self.V.wizard_tower_objs[(17,27)] = bd.WizardTower((17,27), self.V)
        self.V.wall_objs[(0,35)] = bd.Wall((0,35), self.V)

        target = self.V.cannon_objs[(0,15)]
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.hut_objs[(5,0)]
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.wizard_tower_objs[(17,27)]
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.wall_objs[(0,35)]
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")

        target = self.V.town_hall_obj
        self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
        self.assertEqual(0, target.health, "Health not correct")


    def test_dead_behaviour(self):
        """ensure that king cannot do anything when he is dead"""
        self.King.alive = False
        for target in (self.V.cannon_objs[(0,15)], self.V.hut_objs[(5,0)], self.V.wizard_tower_objs[(17,27)],
                       self.V.town_hall_obj, self.V.wall_objs[(0,35)]):
            init_health = target.health
            self.assertEqual(self.King.attack_target(target, 2), None, "Return Value not None")
            self.assertEqual(init_health, target.health, "Health changed")
            self.assertFalse(target.destroyed, "Destroyed state changed")
            
            target.health -= 2
            init_health = target.health
            self.assertEqual(self.King.attack_target(target, 2), None, "Return Value not None")
            self.assertEqual(init_health, target.health, "Health changed")
            self.assertFalse(target.destroyed, "Destroyed state changed")

            self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
            self.assertEqual(init_health, target.health, "Health changed")
            self.assertFalse(target.destroyed, "Destroyed state changed")


    def test_changes_not_allowed(self):
        """ensure king.attack_target cannot change some attributes of Target and King"""
        k = self.King
        for target in (self.V.cannon_objs[(0,15)], self.V.hut_objs[(5,0)], self.V.wizard_tower_objs[(17,27)],
                       self.V.town_hall_obj, self.V.wall_objs[(0,35)]):
            for alive in (False, True):
                k.alive = alive
                king_init = [k.speed,k.health,k.max_health,k.attack,k.AoE,k.facing,k.attack_radius,
                             k.position,k.alive]
                target_init = [target.position, target.dimensions, target.max_health, target.type]
                try:
                    target_init += [target.attack, target.attack_radius]
                except:
                    pass                
                self.assertEqual(self.King.attack_target(target, 2), None, "Return Value not None")
                king_fin = [k.speed,k.health,k.max_health,k.attack,k.AoE,k.facing,k.attack_radius,
                             k.position,k.alive]
                self.assertEqual(king_init, king_fin, "King attributes changed")
                target_fin = [target.position, target.dimensions, target.max_health, target.type]
                try:
                    target_fin += [target.attack, target.attack_radius]
                except:
                    pass
                self.assertEqual(target_init, target_fin, "Target attributes changed") 
                
                target.health -= 2
                self.assertEqual(self.King.attack_target(target, 2), None, "Return Value not None")
                king_fin = [k.speed,k.health,k.max_health,k.attack,k.AoE,k.facing,k.attack_radius,
                             k.position,k.alive]
                self.assertEqual(king_init, king_fin, "King attributes changed")
                target_fin = [target.position, target.dimensions, target.max_health, target.type]
                try:
                    target_fin += [target.attack, target.attack_radius]
                except:
                    pass
                self.assertEqual(target_init, target_fin, "Target attributes changed")

                self.assertEqual(self.King.attack_target(target, 150), None, "Return Value not None")
                king_fin = [k.speed,k.health,k.max_health,k.attack,k.AoE,k.facing,k.attack_radius,
                             k.position,k.alive]
                self.assertEqual(king_init, king_fin, "King attributes changed")
                target_fin = [target.position, target.dimensions, target.max_health, target.type]
                try:
                    target_fin += [target.attack, target.attack_radius]
                except:
                    pass
                self.assertEqual(target_init, target_fin, "Target attributes changed")


with open("temp_bonus.txt", "w") as sys.stderr:
    unittest.main(exit=False)

with open("temp_bonus.txt") as f:
    string = f.readline().strip()
    s = '.' * len(string)

os.remove("temp_bonus.txt")

with open("output_bonus.txt", "w") as f:
    if s == string:
        f.write("True")
    else:
        f.write("False")