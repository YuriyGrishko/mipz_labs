from typing import List
from .city import City


class Country:
    def __init__(self, name: str):
        self.name = name
        self.cities: List[City] = []
        self.full = False
        self.day_of_full = -1

    def __eq__(self, other):
        return self.day_of_full == other.day_of_full

    def __lt__(self, other):
        return self.day_of_full < other.day_of_full

    def append_city(self, city: City) -> None:
        self.cities.append(city)

    def check_fullness(self, day) -> None:
        if self.full:
            return
        for city in self.cities:
            if city.full is False:
                return
        self.full = True
        self.day_of_full = day

    def has_foreign_neighbours(self) -> bool:
        for city in self.cities:
            for neighbour in city.neighbours:
                if neighbour.country_name != self.name:
                    return True

    def only_country_mode(self) -> None:
        self.full = True
        self.day_of_full = 0
