import sys


class Ring:
    def __init__(
        self, start_lat, start_lon, azim, end_lat, end_lon, resolution, width, interval
    ):

        self.start_point = Point(start_lat, start_lon)
        self.end_point = Point(end_lat, end_lon)
        self.azim = azim

        self.resolution = resolution
        self.width = width
        self.interval = interval

        self.perpendiculars = []
        self.num_perpendiculars = 0

        self.points = []
        self.num_points = 0

        self.index_pops = []

        # pyplot globe paths
        self.paths = {}
        self.num_paths = 0

        self.population = 0

        self.country_pop = {}

        self.path_calculation_time = 0
        self.population_calculation_time = 0

    def getsize(self):
        size = sys.getsizeof(self)
        size += sys.getsizeof(self.points)
        size += sys.getsizeof(self.perpendiculars)

        return size / (2 ** 20)


class Point:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

