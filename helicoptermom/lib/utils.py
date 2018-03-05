import sys
from helicoptermom.lib.gameobjects import MAP_SNAKE


def print_matrix(matrix):
    """Print a 2D matrix to the console."""
    for ylist in matrix:
        for item in ylist:
            sys.stdout.write(str(item) + " ")
        print()


def neighbors_of(x, y, map):
    """Get the neighboring cells of a given cell. Excludes cells that are
    outside the boundaries of the world.
    :param x: X coordinate of cell
    :param y: Y coordinate of cell
    :param map: Map containing the cell.
    :return Iterator of all neighboring cells.
    """
    assert 0 <= x < map.shape[1], "X coordinate must be in bounds!"
    assert 0 <= y < map.shape[0], "Y coordinate must be in bounds!"

    if x + 1 < map.shape[1] and map[y][x+1] != MAP_SNAKE:
        yield x + 1, y
    if y + 1 < map.shape[0] and map[y+1][x] != MAP_SNAKE:
        yield x, y + 1
    if x - 1 >= 0 and map[y][x-1] != MAP_SNAKE:
        yield x - 1, y
    if y - 1 >= 0 and map[y-1][x] != MAP_SNAKE:
        yield x, y - 1
