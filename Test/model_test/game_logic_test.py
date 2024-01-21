"""!
@package Test
@package model_test
@file game_logic_test.py
@desc This file contains the tests of the core of the game
"""

import unittest

import model.game_logic as model
from model.game_types import StackPos_t


class MyCoreTest(unittest.TestCase):
    """! @class MyCoreTest
    @brief This class is used to test the core of the game
    """

    def test_valid_coord(self):
        """! @fn test_valid_coord
        @brief This function is used to test the validity of the coordinates
        """
        self.assertTrue(model.mod_valid_coord(2, 3, 5, 7))
        self.assertTrue(model.mod_valid_coord(0, 0, 5, 7))
        self.assertFalse(model.mod_valid_coord(6, 8, 5, 7))
        self.assertFalse(model.mod_valid_coord(-1, 3, 5, 7))

    def test_finish_range_horizontal(self):
        # Create a sample grid
        #  in fact, vertical is the grid in vertical way
        """! @fn test_finish_range_horizontal
        @brief This function is used to test the validity of the horizontal
        range
        """
        grid = [
            [1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1],
            [1, 0, -1, 0, 0],
            [1, 1, 0, 1, 1],
            [1, -1, -1, -1, -1],
        ]

        # false means there is a victory
        (self.assertTrue(model.mod_finish_range_horizontal(1,
                                                           0, 0,
                                                           grid, 3,
                                                           5,
                                                           5)))
        # true means there is either a victory or draw
        self.assertFalse(
            model.mod_finish_range_horizontal(0, 2, 1, grid,
                                              3, 5, 5))

    def test_finish_range_vertical(self):
        # Create a sample grid
        #  in fact, vertical is the grid in horizontal way
        """! @fn test_finish_range_vertical
        @brief This function is used to test the validity of the vertical
        range
        """
        grid = [
            [-1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1],
            [0, 0, -1, 0, 0],
            [1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1],
        ]

        self.assertTrue(
            model.mod_finish_range_vertical(1, 3, 0,
                                            grid, 4, 5,
                                            5))
        self.assertFalse(
            model.mod_finish_range_vertical(0, 2,
                                            1, grid, 4, 5,
                                            5))

    def test_finish_range_bas_gauche(self):
        # Create a sample grid
        """! @fn test_finish_range_bas_gauche
        @brief This function is used to test the validity of the diagonal
        range
        """
        grid = [
            [-1, 0, 0, 1, 0],
            [-1, 1, 1, 0, 0],
            [0, -1, 0, 0, 1],
            [-1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
        ]

        self.assertTrue(
            model.mod_finish_range_bas_gauche(0, 0,
                                              4, grid, 5,
                                              5, 5))
        self.assertFalse(
            model.mod_finish_range_bas_gauche(1, 1, 1, grid,
                                              5, 5, 5))

    def test_finish_range_haut_gauche(self):
        # Create a sample grid
        """! @fn test_finish_range_haut_gauche
        @brief This function is used to test the validity of the diagonal
        range
        """
        grid = [
            [1, 0, 0, 1, 1],
            [-1, 1, 0, 1, 0],
            [0, -1, 1, 0, 1],
            [0, 0, 1, 1, 0],
            [-1, -1, -1, 0, 1],
        ]

        self.assertTrue(
            model.mod_finish_range_haut_gauche(1, 1, 1, grid,
                                               5, 5, 5))
        self.assertFalse(
            model.mod_finish_range_haut_gauche(0, 0, 2, grid,
                                               5, 5, 5))

    def test_finish_range_in_all_directions(self):
        # Create a sample grid
        """! @fn test_finish_range_in_all_directions
        @brief This function is used to test the validity of the diagonal
        range
        """
        grid = [
            [-1, 0, 0, 1, 1],
            [-1, 1, 0, 1, 0],
            [0, -1, 0, 0, 1],
            [0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]

        # false means there is a victory
        # true means there is either a victory or draw

        self.assertTrue(
            model.mod_finish_range_in_all_directions(1, 4, 0,
                                                     grid,
                                                     5, 5, 5)
        )
        self.assertFalse(
            model.mod_finish_range_in_all_directions(1, 0, 1,
                                                     grid,
                                                     5, 5, 5)
        )

    def test_play_bot(self):
        """! @fn test_play_bot
        @brief This function is used to test the validity of the bot's play
        """
        grid = [
            [-1, 0, 0, 1, 0],
            [-1, 1, 1, 0, 0],
            [0, -1, 0, 0, 1],
            [-1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
        ]

        # false means there is a victory
        # true means there is either a victory or draw

        self.assertTrue(model.mod_play_bot(grid, 0, True,
                                           5,
                                           5, 5, [2, 0]))
        self.assertFalse(model.mod_play_bot(grid, 0, True,
                                            5,
                                            5, 5, [4, 0]))

    def test_play_human(self):
        """! @fn test_play_human
        @brief This function is used to test the validity of the human's play
        """
        grid = [
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, -1, 0, 0, 1],
            [1, 0, 1, 1, 0],
            [1, 1, 1, 0, 1],
        ]

        self.assertTrue(model.mod_play_human(grid, 1, [1, 1],
                                             True, 5,
                                             5, 5))
        self.assertFalse(model.mod_play_human(grid, 1, [0, 0],
                                              True, 5,
                                              5, 5))

    def test_peek(self):
        """! @fn test_peek
        @brief This function is used to test the validity of the peek
        """
        stack1: StackPos_t = [[1, 2], [4, 5]]
        stack2: StackPos_t = []
        self.assertEqual(model.mod_peek(stack1), [4, 5])
        self.assertNotEqual(model.mod_peek(stack1), [1, 2])
        self.assertIsNone(model.mod_peek(stack2))
        self.assertIsNotNone(model.mod_peek(stack1))

    def test_launch_game(self):
        """! @fn test_launch_game
        @brief This function is used to test the validity of the launch game
        """
        grid = [
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, -1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 1, 1, 0, 0],
        ]
        # testing the tourJeu value to match player's round

        # human's tour
        self.assertFalse(model.mod_launch_game(grid, 5, 5,
                                               8, 5,
                                               True, [0, 0]))
        # bot's tour
        self.assertFalse(model.mod_launch_game(grid, 5, 5,
                                               5, 5,
                                               True, [0, 4]))

        # human's tour
        self.assertTrue(model.mod_launch_game(grid, 5, 5,
                                              2, 5,
                                              True, [1, 1]))
        # Bot's tour
        self.assertTrue(model.mod_launch_game(grid, 5, 5,
                                              17, 5,
                                              True, [0, 1]))


if __name__ == "__main__":
    """! @fn __main__
    @brief This function is used to test the validity of the core of the game
    """
    unittest.main()
