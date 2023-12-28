import unittest

from model.core import *


class MyCoreTest(unittest.TestCase):
    def test_valid_coord(self):
        self.assertTrue(valid_coord(2, 3, 5, 7))
        self.assertTrue(valid_coord(0, 0, 5, 7))
        self.assertFalse(valid_coord(6, 8, 5, 7))
        self.assertFalse(valid_coord(-1, 3, 5, 7))

    def test_finish_range_horizontal(self):
        # Create a sample grid
        #  in fact, vertical is the grid in vertical way
        grid = [
            [1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1],
            [1, 0, -1, 0, 0],
            [1, 1, 0, 1, 1],
            [1, -1, -1, -1, -1],
        ]

        self.assertTrue(finish_range_horizontal(1, 0, 0, grid, 3, 5, 5))
        self.assertFalse(finish_range_horizontal(0, 2, 1, grid, 3, 5, 5))

    def test_finish_range_vertical(self):
        # Create a sample grid
        #  in fact, vertical is the grid in horizontal way
        grid = [
            [-1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1],
            [0, 0, -1, 0, 0],
            [1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1],
        ]

        self.assertTrue(finish_range_vertical(1, 3, 0, grid, 4, 5, 5))
        self.assertFalse(finish_range_vertical(0, 2, 1, grid, 4, 5, 5))

    def test_finish_range_bas_gauche(self):
        # Create a sample grid
        grid = [
            [-1, 0, 0, 1, 0],
            [-1, 1, 1, 0, 0],
            [0, -1, 0, 0, 1],
            [-1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
        ]

        self.assertTrue(finish_range_bas_gauche(0, 0, 4, grid, 5, 5, 5))
        self.assertFalse(finish_range_bas_gauche(1, 1, 1, grid, 5, 5, 5))

    def test_finish_range_haut_gauche(self):
        # Create a sample grid
        grid = [
            [1, 0, 0, 1, 1],
            [-1, 1, 0, 1, 0],
            [0, -1, 1, 0, 1],
            [0, 0, 1, 1, 0],
            [-1, -1, -1, 0, 1],
        ]

        self.assertTrue(finish_range_haut_gauche(1, 1, 1, grid, 5, 5, 5))
        self.assertFalse(finish_range_haut_gauche(0, 0, 2, grid, 5, 5, 5))

    def test_finish_range_in_all_directions(self):
        # Create a sample grid

        grid = [
            [-1, 0, 0, 1, 1],
            [-1, 1, 0, 1, 0],
            [0, -1, 0, 0, 1],
            [0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]

        # false means there is a victory
        # true means there is either a victory or draw

        self.assertTrue(finish_range_in_all_directions(1, 4, 0, grid, 5, 5, 5))
        self.assertFalse(finish_range_in_all_directions(1, 0, 1, grid, 5, 5, 5))

    def test_play_bot(self):
        grid = [
            [-1, 0, 0, 1, 0],
            [-1, 1, 1, 0, 0],
            [0, -1, 0, 0, 1],
            [-1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
        ]

        # false means there is a victory
        # true means there is either a victory or draw

        self.assertTrue(play_bot(grid, 0, True, 5, 5, 5, [2, 0]))
        self.assertFalse(play_bot(grid, 0, True, 5, 5, 5, [4, 0]))

    def test_play_human(self):
        grid = [
            [1, 0, 0, 1, 0],
            [1, 1, 1, 0, 0],
            [1, -1, 0, 0, 1],
            [1, 0, 1, 1, 0],
            [1, 1, 1, 0, 1],
        ]

        self.assertTrue(play_human(grid, 1, [1, 1], True, 5, 5, 5))
        self.assertFalse(play_human(grid, 1, [0, 0], True, 5, 5, 5))


if __name__ == "__main__":
    unittest.main()
