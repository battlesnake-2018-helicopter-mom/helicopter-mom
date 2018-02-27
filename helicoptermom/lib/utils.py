import sys


def print_matrix(matrix):
    """Print a 2D matrix to the console."""
    for ylist in matrix:
        for item in ylist:
            sys.stdout.write(str(item) + " ")
        print()


def neighbors_of(x, y, world):
    """Get the neighboring cells of a given cell. Excludes cells that are
    outside the boundaries of the world.
    :param x: X coordinate of cell
    :param y: Y coordinate of cell
    :param world: World map containing the cell.
    :return Iterator of all neighboring cells.
    """
    assert 0 <= x < world.width, "X coordinate must be in bounds!"
    assert 0 <= y < world.height, "Y coordinate must be in bounds!"

    if x + 1 < world.width:
        yield x + 1, y
    if y + 1 < world.height:
        yield x, y + 1
    if x - 1 >= 0:
        yield x - 1, y
    if y - 1 >= 0:
        yield x, y - 1
