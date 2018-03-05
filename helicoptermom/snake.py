"""
Pretty dumb Dijkstra snake, but makes use of a bunch of handy-dandy utility
functions and classes I wrote, so good example usage for those interested.
:author Charlie
"""
import bottle
import logging
from bottle import request
import numpy as np

import helicoptermom.lib.pathfinding as pathfinding
from helicoptermom.lib.gameobjects import World
from helicoptermom.lib.utils import neighbors_of

app = bottle.app()


@app.post("/start")
def start():
    return {
        "name": "Helicopter Mom",
        "taunt": "Can I see your manager?",
        "color": "#03A9F4",
        "head_type": "tongue",
        "tail_type": "block-bum",
        "head_url": "https://s3-us-west-2.amazonaws.com/flx-editorial-wordpress/wp-content/uploads/2016/01/19133540/seinfeld.jpg"
    }


def vornoi_defense(world):
    # Calculate d matrices for every snake
    d_matrices = {}
    enemy_snakes = [snake for snake in world.snakes.values() if snake.id != world.you.id]
    for snake in enemy_snakes:
        d_matrix = pathfinding.dijkstra(world.map, snake.head)
        d_matrices.update({snake.id: d_matrix})

    # For each option, simulate snake move and calculate Vornoi zones
    highest_vornoi_area = -1
    highest_scoring_option = None
    for next_point in neighbors_of(world.you.head[0], world.you.head[1], world.map):
        np_scores, predecessor = pathfinding.dijkstra(world.map, next_point)
        in_vornoi_zone = np.full((world.height, world.width), True, dtype=np.bool)

        # Get all points in your Vornoi zone
        for val in d_matrices.values():
            in_vornoi_zone = np.logical_and(in_vornoi_zone, val - np_scores > 0)

        vornoi_area = np.sum(in_vornoi_zone)
        if vornoi_area > highest_vornoi_area:
            highest_vornoi_area = vornoi_area
            highest_scoring_option = next_point

    return pathfinding.get_next_move(world.you.head, [highest_scoring_option])


def hungry_mode(world):
    """ Used when we need food. Dijkstra to nearest food. """
    distance, predecessor = pathfinding.dijkstra(world.map, world.you.head)

    nearest_food = None
    closest_distance = np.inf
    for fx, fy in world.food:
        if distance[fy][fx] < closest_distance and pathfinding.is_safe(fx, fy, world, predecessor):
            closest_distance = distance[fy][fx]
            nearest_food = (fx, fy)

    if closest_distance == np.inf:
        # If we can't get to any food, use defense mode
        return vornoi_defense(world)
    else:
        path = pathfinding.find_path_dijkstra(nearest_food[0], nearest_food[1], predecessor)
        return pathfinding.get_next_move(world.you.head, path)


@app.post("/move")
def move():
    world = World(request.json)

    longest_snake = max(world.snakes.values(), key=lambda s: s.length)
    if world.you.health < 60 or world.you.length < longest_snake.length:
        next_move = hungry_mode(world)
    else:
        next_move = vornoi_defense(world)

    return {
        "move": next_move
    }


if __name__ == "__main__":
    app.run(port=8000)
