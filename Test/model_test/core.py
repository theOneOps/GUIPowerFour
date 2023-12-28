import unittest
from model.core import *


class MyTestCase(unittest.TestCase):
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

    def test_finish_range_haut_gauche(self):
        # Create a sample grid
        grid = [
            [-1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1],
            [0, 0, -1, 0, 0],
            [1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1],
        ]
        self.assertTrue(finish_range_haut_gauche())
        self.assertTrue(finish_range_haut_gauche())

    def test_finish_range_bas_gauche(self):
        # Create a sample grid
        grid = [
            [-1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1],
            [0, 0, -1, 0, 0],
            [1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1],
        ]
        self.assertTrue(finish_range_bas_gauche())
        self.assertTrue(finish_range_bas_gauche())

    def test_finish_range_in_all_directions(self):
        # Create a sample grid

        self.assertTrue(finish_range_in_all_directions())
        self.assertTrue(finish_range_in_all_directions())


if __name__ == "__main__":
    unittest.main()
