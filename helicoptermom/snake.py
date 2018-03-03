"""
Pretty dumb Dijkstra snake, but makes use of a bunch of handy-dandy utility
functions and classes I wrote, so good example usage for those interested.
:author Charlie
"""
import bottle
import logging
from bottle import request

import helicoptermom.lib.pathfinding as pathfinding
from helicoptermom.lib.gameobjects import World

app = bottle.app()


@app.post("/start")
def start():
    return {
        "name": "Dijkstrasnek",
        "taunt": "Booo application. Yay theory!",
        "color": "#03A9F4",
        "head_type": "tongue",
        "tail_type": "block-bum"
    }


@app.post("/move")
def move():

    world = World(request.json)

    # Consider all food - where would I have to go to get it?
    next_point_options = set()
    dijkstra_scores, predecessor = pathfinding.dijkstra(world, world.you.head)
    for food_x, food_y in world.food:
        path = pathfinding.find_path_dijkstra(food_x, food_y, predecessor)
        next_point_options.add(path[0])  # only get the NEXT path location

    # # For each option, simulate snake move and calculate Vornoi zones
    # highest_vornoi_area = -1
    # highest_scoring_option = None
    # for next_point in next_point_options:
    #     np_scores, predecessor = pathfinding.dijkstra(world, next_point)


    nextfood_x, nextfood_y = world.food[0]
    path = pathfinding.find_path_dijkstra(nextfood_x, nextfood_y, predecessor)
    next_move = pathfinding.get_next_move(world.you.head, path)

    return {
        "move": next_move
    }


if __name__ == "__main__":
    app.run(port=8000)
