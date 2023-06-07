import unittest, sys, os
import king, village, points as pt, buildings as bd

class TestKingMove(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """initialize the village and king"""
        self.V = village.createVillage(1)
        self.King = king.getHero(0)


    def setUp(self):
        """make sure the king is alive before each unit test"""
        self.King.alive = True
        # self.King.speed = 2


    def test_move_in_correct_direction(self):
        """ensure that king goes in the correct direction"""
        for speed in (1,2,4):
            for r in range(self.V.dimensions[0]):
                for c in range(self.V.dimensions[1]):
                    for direction in ("up", "down", "left", "right"):
                        self.King.position = [r,c]
                        self.King.speed = speed
                        self.assertEqual(self.King.move(direction, self.V), None, "Return Value not None")
                        if direction == 'up':
                            self.assertEqual(self.King.position[1], c, "Column changed")
                            self.assertLessEqual(self.King.position[0], r, "Moved in opposite direction")
                        elif direction == 'down':
                            self.assertEqual(self.King.position[1], c, "Column changed")
                            self.assertGreaterEqual(self.King.position[0], r, "Moved in opposite direction")
                        if direction == 'left':
                            self.assertEqual(self.King.position[0], r, "Row changed")
                            self.assertLessEqual(self.King.position[1], c, "Moved in opposite direction")
                        if direction == 'right':
                            self.assertEqual(self.King.position[0], r, "Row changed")
                            self.assertGreaterEqual(self.King.position[1], c, "Moved in opposite direction")


    def test_positions_match(self):
        """ensure that pt.HERO_POS is the same as self.position"""
        for speed in (1,2,4):
            for r in range(self.V.dimensions[0]):
                for c in range(self.V.dimensions[1]):
                    for direction in ("up", "down", "left", "right"):
                        self.King.position = [r,c]
                        self.King.speed = speed
                        self.assertEqual(self.King.move(direction, self.V), None, "Return Value not None")
                        self.assertEqual(pt.HERO_POS, self.King.position, "Position do not match")


    def test_wrong_index(self):
        """ensure that position of king does not go out of bounds of map"""
        r,c = self.V.dimensions
        up_pos = ([0,0], [0,2], [1,1])
        left_pos = ([0,0], [2,0], [1,1])
        down_pos = ([r-1,c-1], [r-1,c-3], [r-2,c-2])
        right_pos = ([r-1,c-1], [r-3,c-1], [r-2,c-2])

        for speed in (1,2,4):
            self.King.speed = speed

            for i in up_pos:
                self.King.position = i
                self.assertEqual(self.King.move("up", self.V), None, "Return Value not None")
                self.assertGreaterEqual(self.King.position[0], 0, "Negative index")

            for i in left_pos:
                self.King.position = i
                self.assertEqual(self.King.move("left", self.V), None, "Return Value not None")
                self.assertGreaterEqual(self.King.position[1], 0, "Negative index")

            for i in down_pos:
                self.King.position = i
                self.assertEqual(self.King.move("down", self.V), None, "Return Value not None")
                self.assertLessEqual(self.King.position[0], 17, "Index out of bounds")

            for i in right_pos:
                self.King.position = i
                self.assertEqual(self.King.move("right", self.V), None, "Return Value not None")
                self.assertLessEqual(self.King.position[1], 35, "Index out of bounds")
        

    def test_did_not_go_through_buildings(self):
        """ensure that king doesn't walk through buildings"""
        for speed in (1,2,4):
            for r in range(self.V.dimensions[0]):
                for c in range(self.V.dimensions[1]):
                    self.King.speed = speed

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("up", self.V), None, "Return Value not None")
                    dist = r-self.King.position[0]
                    for i in range(1,dist+1):
                        self.assertIn(self.V.map[r-i][c], (pt.BLANK, pt.SPAWN), "Went through building")

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("down", self.V), None, "Return Value not None")
                    dist = self.King.position[0]-r
                    for i in range(1,dist+1):
                        self.assertIn(self.V.map[r+i][c], (pt.BLANK, pt.SPAWN), "Went through building")

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("left", self.V), None, "Return Value not None")
                    dist = c-self.King.position[1]
                    for i in range(1,dist+1):
                        self.assertIn(self.V.map[r][c-i], (pt.BLANK, pt.SPAWN), "Went through building")

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("right", self.V), None, "Return Value not None")
                    dist = self.King.position[1]-c
                    for i in range(1,dist+1):
                        self.assertIn(self.V.map[r][c+i], (pt.BLANK, pt.SPAWN), "Went through building")


    def test_moved_correct_amount(self):
        """ensure that king moves the correct distance"""
        rows, cols = self.V.dimensions
        for speed in (1,2,4):
            for r in range(rows):
                for c in range(cols):
                    self.King.speed = speed

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("up", self.V), None, "Return Value not None")
                    dist = r-self.King.position[0]
                    self.assertLessEqual(dist, self.King.speed, "Moved more than speed")
                    if dist != self.King.speed and self.King.position[0] != 0:
                        self.assertNotIn(self.V.map[r-dist-1][c], (pt.BLANK, pt.SPAWN), "Stopped early")
                    
                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("left", self.V), None, "Return Value not None")
                    dist = c-self.King.position[1]
                    self.assertLessEqual(dist, self.King.speed, "Moved more than speed")
                    if dist != self.King.speed and self.King.position[1] != 0:
                        self.assertNotIn(self.V.map[r][c-dist-1], (pt.BLANK, pt.SPAWN), "Stopped early")

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("down", self.V), None, "Return Value not None")
                    dist = self.King.position[0]-r
                    self.assertLessEqual(dist, self.King.speed, "Moved more than speed")
                    if dist != self.King.speed and self.King.position[0] != rows-1:
                        self.assertNotIn(self.V.map[r+dist+1][c], (pt.BLANK, pt.SPAWN), "Stopped early")

                    self.King.position = [r,c]
                    self.assertEqual(self.King.move("right", self.V), None, "Return Value not None")
                    dist = self.King.position[1]-c
                    self.assertLessEqual(dist, self.King.speed, "Moved more than speed")
                    if dist != self.King.speed and self.King.position[1] != cols-1:
                        self.assertNotIn(self.V.map[r][c+dist+1], (pt.BLANK, pt.SPAWN), "Stopped early")


    def test_correct_facing_direction(self):
        """ensure that king faces the correct direction when moved"""
        for speed in (1,2,4):
            for r in range(self.V.dimensions[0]):
                for c in range(self.V.dimensions[1]):
                    for direction in ("up", "down", "left", "right"):
                        self.King.position = [r,c]
                        self.King.speed = speed
                        self.assertEqual(self.King.move(direction, self.V), None, "Return Value not None")
                        self.assertEqual(self.King.facing, direction, "Facing Direction Wrong")


    def test_dead_behaviour(self):
        """ensure that king cannot do anything when he is dead"""
        self.King.alive = False
        for speed in (1,2,4):
            for initial_facing_direction in ("up", "down", "left", "right"):
                for r in range(self.V.dimensions[0]):
                    for c in range(self.V.dimensions[1]):
                        self.King.speed = speed
                        self.King.position = [r,c]
                        pt.HERO_POS = [r,c]
                        self.King.facing = initial_facing_direction
                        for direction in ("up", "down", "left", "right"):
                            self.assertEqual(self.King.move(direction, self.V), None, "Return Value not None")
                            self.assertEqual(pt.HERO_POS, [r,c], "Position Changed")
                            self.assertEqual(self.King.position, [r,c], "Position Changed")
                            self.assertEqual(self.King.facing, initial_facing_direction, "Facing Direction Changed")


    def test_changes_not_allowed(self):
        """ensure king.move cannot change some attributes of Village and King"""
        k = self.King
        # v = self.V
        for speed in (1,2,4):
            for alive in (True, False):
                for initial_facing_direction in ("up", "down", "left", "right"):
                    for r in range(self.V.dimensions[0]):
                        for c in range(self.V.dimensions[1]):
                            k.speed = speed
                            k.alive = alive
                            k.facing = initial_facing_direction
                            king_init = [k.speed,k.health,k.max_health,k.attack,k.AoE,k.attack_radius,k.alive]
                            # vill_init = [{},{},{},{},v.level,v.dimensions]
                            # vill_init[0].update(v.hut_objs)
                            # vill_init[1].update(v.cannon_objs)
                            # vill_init[2].update(v.wizard_tower_objs)
                            # vill_init[3].update(v.wall_objs)
                            for direction in ("up", "down", "left", "right"):
                                k.position = [r,c]
                                self.assertEqual(self.King.move(direction, self.V), None, "Return Value not None")
                                king_fin = [k.speed,k.health,k.max_health,k.attack,k.AoE,k.attack_radius,k.alive]
                                self.assertEqual(king_init, king_fin, "King attributes changed")

                                # vill_fin = [v.hut_objs,v.cannon_objs,v.wizard_tower_objs,v.wall_objs,
                                #             v.level,v.dimensions]
                                # self.assertEqual(vill_init,vill_fin,"Village attributes changed")


    def test_invalid_direction(self):
        """ensure that nothing changes if invalid input direction is given"""
        for speed in (1,2,4):
            for r in range(self.V.dimensions[0]):
                for c in range(self.V.dimensions[1]):
                    self.King.speed = speed
                    self.King.position = [r,c]
                    pt.HERO_POS = [r,c]
                    self.assertEqual(self.King.move("random", self.V), None, "Return Value not None")
                    self.assertEqual(self.King.position, [r,c], "Position changed")
                    self.assertEqual(pt.HERO_POS, [r,c], "Position changed")


with open("temp.txt", "w") as sys.stderr:
    unittest.main(exit=False)

with open("temp.txt") as f:
    string = f.readline().strip()
    s = '.' * len(string)

os.remove("temp.txt")

with open("output.txt", "w") as f:
    if s == string:
        f.write("True")
    else:
        f.write("False")