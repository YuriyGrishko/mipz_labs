from typing import List
from .country import Country
from .city import City
from .config import grid_size


class Map:
    def __init__(self, countries_data):
        self.countries = []
        self.grid: List[List[City]] = [[None] * (grid_size + 2) for i in range((grid_size + 2))]
        self.__initialize_grid(countries_data)
        self.__validate_foreign_neighbours()

    def simulate_euro_diffusion(self) -> None:
        # check length of countries, if it's 1, country is already full
        if len(self.countries) == 1:
            self.countries[0].only_county_mode()
            return

        full = False
        day = 1
        while not full:
            for x in range(grid_size + 1):
                for y in range(grid_size + 1):
                    if self.grid[x][y] is not None:
                        city = self.grid[x][y]
                        city.transfer_to_neighbours()

            for x in range(grid_size + 1):
                for y in range(grid_size + 1):
                    if self.grid[x][y] is not None:
                        city = self.grid[x][y]
                        city.finalize_balance_per_day()

            full = True
            for country in self.countries:
                country.check_fullness(day)
                if country.full is False:
                    full = False

            # if not full:
            day += 1

        self.countries.sort()

    def __initialize_grid(self, countries_data) -> None:
        # go through every country and put it's cities on the grid
        for country_data in countries_data:
            country = Country(country_data["name"])
            for x in range(country_data["lowerLeft"]["x"], country_data["upperRight"]["x"] + 1):
                for y in range(country_data["lowerLeft"]["y"], country_data["upperRight"]["y"] + 1):
                    if self.grid[x][y] is not None:
                        raise Exception("%s intersects with %s on [%i, %i]" %
                                        (self.grid[x][y].country_name, country.name, x, y))
                    city = City(country.name, countries_data, x, y)
                    self.grid[x][y] = city
                    # add this city to country
                    country.append_city(city)
            self.countries.append(country)

        # set neighbours for each city
        for row in self.grid:
            for city in row:
                if city is not None:
                    neighbours_list = self.__get_neighbours(city.x, city.y)
                    city.set_neighbours(neighbours_list)

    def __get_neighbours(self, x, y) -> List[City]:
        neighbours = []
        if self.__check_if_neighbour_exists(x, y + 1):
            neighbours.append(self.grid[x][y + 1])
        if self.__check_if_neighbour_exists(x, y - 1):
            neighbours.append(self.grid[x][y - 1])
        if self.__check_if_neighbour_exists(x + 1, y):
            neighbours.append(self.grid[x + 1][y])
        if self.__check_if_neighbour_exists(x - 1, y):
            neighbours.append(self.grid[x - 1][y])
        return neighbours

    def __check_if_neighbour_exists(self, x, y):
        return self.grid[x][y] is not None

    def __validate_foreign_neighbours(self) -> None:
        if len(self.countries) <= 1:
            return
        for country in self.countries:
            if not country.has_foreign_neighbours():
                raise Exception("%s has no connection with other countries" % country.name)

