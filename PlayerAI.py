from PythonClientAPI.Game import PointUtils
from PythonClientAPI.Game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.Game.Enums import Direction, MoveType, MoveResult
from PythonClientAPI.Game.World import World

class PlayerAI:

    def __init__(self):
        self.setup_phase = True
        self.width = None
        self.height = None
        self.target_nests = set()
        self.turn_count = 0
        self.nest_count = 0
        self.wall_count = 0

    def do_move(self, world, friendly_units, enemy_units):
        if self.setup_phase == True:
            # this if block will compute the optimal packing of one-nest
            # clusters for this map. these are tiles we don't want to step
            # on so we can turn them into nests. these tiles are stored
            # as self.target_nests.
            candidate_grids = [set() for k in range(5)]
            self.width, self.height = world.get_width(), world.get_height()
            for i in range(self.height):
                for j in range(self.width):
                    if j % 5 == ((2 * i) % 5):
                        self.target_nests.add((i,j))
            tile_positions, walls = [], set()
            for i in range(self.height):
                for j in range(self.width):
                    if world.is_wall((i, j)):
                        walls.add((i,j))
            nest_positions = world.get_friendly_nest_positions()
            self.wall_count = len(list(walls))
            self.setup_phase = False


        # if < 5% of tiles are neutral go completely greedy.
        if (len(world.get_neutral_tiles()) / (self.width * self.height - self.wall_count)) < 0.05:
            self.target_nests = set()

        for unit in friendly_units:
            path = world.get_shortest_path(unit.position,
                                        world.get_closest_capturable_tile_from(unit.position, self.target_nests).position,
                                        self.target_nests)
            if path: world.move(unit, path[0])
