"""
Classes representing objects in the game (parsed from JSON).
"""

import numpy as np

MAP_EMPTY = 0
MAP_SNAKE = 1
MAP_FOOD  = 2


class Snake:
    def __init__(self, snake_json):
        """Create new snake from a json payload."""
        self.id = snake_json["id"]
        self.name = snake_json["name"]
        self.health = int(snake_json["health"])
        self.length = int(snake_json["length"])

        self.body = [(int(point['x']), int(point['y'])) for point in snake_json["body"]["data"]]

        # According to Corey, the snake's head should be the 0th element of its body.
        # I'm still kinda wary of this, but should be ok for the time being :-/
        self.head = self.body[0]


class World:
    def __init__(self, request_json):
        """Create a new world from a /move request payload."""
        self.id = request_json["id"]
        self.width = request_json["width"]
        self.height = request_json["height"]
        self.turn = request_json["turn"]

        # define and populate world map
        self.map = np.full((self.height, self.width), MAP_EMPTY)

        self.food = []
        for food_data in request_json["food"]["data"]:
            self.food.append((int(food_data["x"]), int(food_data["y"])))
            self.map[food_data["y"]][food_data["x"]] = MAP_FOOD

        # snakes are stored in a dictionary indexed by snake id
        self.snakes = {}
        for snake_data in request_json["snakes"]["data"]:
            new_snake = Snake(snake_data)
            self.snakes.update({snake_data["id"]: new_snake})

            for body_point in new_snake.body:
                self.map[body_point[1]][body_point[0]] = MAP_SNAKE

        # get your snake by reference (API copies your snake's data)
        self.you = self.snakes[request_json["you"]["id"]]
