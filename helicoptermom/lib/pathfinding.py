"""
Assorted pathfinding algorithms.
"""

import math
import numpy as np
from heapq import heapify, heappop, heappush

import helicoptermom.lib.gameobjects as objects
from helicoptermom.lib.utils import neighbors_of


def get_next_move(snake_head, path):
    """Get the snake's next move in a given path.
    :param snake_head: Location of the snake's head (x, y).
    :param path: List of points creating a path from the snake's head.
                 [ (x, y), (x, y) ... ]
    :return Next move. One of ("right", "left", "up", "down").
    """
    assert type(path) == list, "Path must be a list."
    assert len(path) > 0, "Cannot get next move for an empty path."

    snakehead_x, snakehead_y = snake_head
    nextpoint_x, nextpoint_y = path[0]
    assert type(nextpoint_x) == int, "Invalid X coordinate."
    assert type(nextpoint_y) == int, "Invalid Y coordinate."
    assert type(snakehead_x) == int, "Invalid X coordinate."
    assert type(snakehead_y) == int, "Invalid Y coordinate."

    assert snake_head != path[0], "Next coordinate cannot be the same as snake head"

    if nextpoint_x > snakehead_x:
        return "right"
    elif nextpoint_x < snakehead_x:
        return "left"
    elif nextpoint_y < snakehead_y:
        return "up"
    elif nextpoint_y > snakehead_y:
        return "down"


def find_path_dijkstra(x, y, p):
    """Get the shortest path to a given point in a predecessor matrix.
    :param x: X coordinate of destination
    :param y: Y coordinate of destination
    :param p: Predecessor matrix to get path from.
    :return List of points in path, starting from snake head [(0, 0),(0, 1)...]
    """
    path = []
    point = p[y][x]

    path.append((x, y))

    while point != -1:
        px, py = int(point % p.shape[0]), int(point / p.shape[0])
        path.append((px, py))
        point = p[py][px]

    path.reverse()
    return path[1:]


def dijkstra(world, point):
    """Gets the distance "scores" and predecessor matrix from a given snake's
    head.
    :param world: World object to map for the snake.
    :param point: Snake to calculate distances from.
    :return: d[] and p[] matrices for each point on the map.
        - p[] matrix uses integers as vertex labels: (y * width) + x
        - None indicates the head of the snake (source node).
        - -1 indicates an inaccessible point.
    """
    d = np.full((world.width, world.height), np.inf)
    p = np.full((world.width, world.height), -1)
    visited = np.full((world.width, world.height), False, dtype=np.bool)

    # d at the snake's head should be 0 (we're already there, so no cost!)
    d[point[1]][point[0]] = 0

    pq = [(1, point)]
    heapify(pq)
    while len(pq) > 0:
        next_vert = heappop(pq)[1]
        nv_x, nv_y = next_vert[0], next_vert[1]

        # ignore if we've already visited this vertex
        if visited[nv_y][nv_x]:
            continue

        # consider neighbors of this vertex
        for x, y in neighbors_of(nv_x, nv_y, world):
            if world.map[y][x] == objects.MAP_SNAKE:
                d[y][x] = -1
                p[y][x] = -1
            elif d[nv_y][nv_x] + 1 < d[y][x]:
                d[y][x] = d[nv_y][nv_x] + 1
                p[y][x] = world.width * nv_y + nv_x

                # re-add to pq if d[] was updated
                heappush(pq, (d[y][x], (x, y)))

        visited[nv_y][nv_x] = True

    return d, p


def buffer_snake(world, snake):
    """Creates buffer around snake to prevent self-collision.
    :param snake: List of snake's body pieces' positions
    :return: List of buffered positions
    """

    # Created because thought we might need this at a later date.
    snake_head = snake.body[0] # Assumption cleared. We are correct.

    body_buffer = []

    # Add buffer points for snake
    for body_item in snake.body:
        if (body_item[0] + 1) not in snake.body:
            body_buffer.append(tuple(body_item[0] + 1, body_item[1]))
        elif (body_item[0] - 1) not in snake.body:
            body_buffer.append(tuple(body_item[0] - 1, body_item[1]))
        elif (body_item[1] + 1) not in snake.body:
            body_buffer.append(tuple(body_item[0], body_item[1] + 1))
        elif (body_item[1] - 1) not in snake.body:
            body_buffer.append(tuple(body_item[0], body_item[1] - 1))
        else:
            continue

    # If body_buffer point is outside of grid, remove.
    for item in body_buffer:
        if item[0] > world.width or item[0] < 0:
            body_buffer.remove(item)
        if item[1] > world.height or item[1] < 0:
            body_buffer.remove(item)

    return body_buffer
