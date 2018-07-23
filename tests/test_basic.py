import os
import sys
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), '..','dots_and_squares')))
from dots_and_squares_game import dots_and_squares_game
import unittest
import pygame

class test_dots_and_squares_game(unittest.TestCase):
    """Tests for  functions in dots_and_squares_game. The unit tests are only for the logic in the
    game, and are not checking the pygame usage."""
    @classmethod
    def setUpClass(self):
        pygame.init()
        self.game = dots_and_squares_game()
    
    @classmethod
    def tearDownClass(self):
        self.game.quit()
        pygame.quit()

    def test_get_end_points(self):
        """Testing get_end_points with multiple valid pos tuples"""
        self.assertEqual(self.game.get_end_points((397,122)),((400,100),(400,150)))
        self.assertEqual(self.game.get_end_points((323, 102)),((300, 100), (350, 100)))
        self.assertEqual(self.game.get_end_points((248, 130)),((250, 100), (250, 150)))
        self.assertEqual(self.game.get_end_points((215, 102)),((200, 100), (250, 100)))
        self.assertEqual(self.game.get_end_points((148, 135)),((150, 100), (150, 150)))
        self.assertEqual(self.game.get_end_points((165, 154)),((150, 150), (200,150)))
        self.assertEqual(self.game.get_end_points((95,136)),((100, 100), (100, 150)))

    def test_get_end_points_outside(self):
        """Testing get_end_points with multiple invalid pos tuples"""
        self.assertIsNone(self.game.get_end_points((562,124)))
        self.assertIsNone(self.game.get_end_points((511,83)))
        self.assertIsNone(self.game.get_end_points((88, 529)))
        self.assertIsNone(self.game.get_end_points((277, 565)))
    
    def test_check_square1(self):
        '''Given a list_of_lines already played in the game determine if a new line makes 
        a square or not'''
        self.game.list_of_lines = [((300, 100), (350, 100)), ((250, 150), (250, 200)), ((200, 150), 
            (200, 200)), ((150, 200), (200, 200))]
        self.assertEqual(self.game.check_square(((150, 200), (200, 200))),0)
        self.assertEqual(self.game.check_square(((300, 200), (350, 200))),0)
        self.assertEqual(self.game.check_square(((250, 200), (300, 200))),0)
        self.assertEqual(self.game.check_square(((300, 150), (300, 200))),0)
        self.assertEqual(self.game.check_square(((250, 150), (300, 150))),0)
    
    def test_check_square2(self):
        '''Given a list_of_lines already played in the game determine if a new line makes
        a square or not. Also add the new line to the list_of_lines'''
        self.game.list_of_lines = [((100, 200), (100, 250)), ((100, 250), (100, 300)), ((100, 300), 
            (100, 350)), ((100, 350), (100, 400)), ((100, 400), (100, 450)), ((100, 450), (100, 500)), 
            ((100, 500), (150, 500)), ((150, 450), (150, 500)), ((150, 400), (150, 450)), ((150, 350), 
            (150, 400)), ((150, 300), (150, 350)), ((150, 250), (150, 300)), ((150, 200), (150, 250)), 
            ((100, 200), (150, 200)), ((100, 250), (150, 250))]
        self.assertEqual(self.game.check_square(((100, 250), (150, 250))),1)
        self.game.list_of_lines.append(((100, 250), (150, 250)))
        self.assertEqual(self.game.check_square(((100, 300), (150, 300))),1)
        self.game.list_of_lines.append(((100, 300), (150, 300)))
        self.assertEqual(self.game.check_square(((100, 300), (150, 300))),1)
        self.game.list_of_lines.append(((100, 300), (150, 300)))
        self.assertEqual(self.game.check_square(((100, 350), (150, 350))),1)
        self.assertEqual(self.game.check_square(((550, 450), (550, 500))),0)
        self.assertEqual(self.game.check_square(((500, 100), (550, 100))),0)

    def test_declare_winner(self):
        '''Check if the winner is determined correctly, given the scores'''
        self.game.score["A"] = 7
        self.game.score["B"] = 10
        self.assertEqual(self.game.declare_winner(),"B")
        self.game.score["A"] = 10
        self.game.score["B"] = 7
        self.assertEqual(self.game.declare_winner(),"A")
        self.game.score["A"] = 7
        self.game.score["B"] = 7
        self.assertEqual(self.game.declare_winner(),"Both")

    
if __name__ == '__main__':
    unittest.main(verbosity=2)