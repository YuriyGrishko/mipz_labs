import re
from .config import max_countries_amount, grid_size
from pathlib import Path

data_folder = Path("data/input.txt")
name_pattern = re.compile("[A-Z][a-z]{1,24}$")

def read_lines(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
    return data.split('\n')

def parse_country(line):
    args = line.split(' ')
    if len(args) != 5:
        raise Exception("Error at line {%s}: invalid number of tokens" % line)
    if not name_pattern.match(args[0]):
        raise Exception("Error at line {%s}: invalid country name" % line)
    for i in range(1, 5):
        if int(args[i]) <= 0 or int(args[i]) >= (grid_size + 1):
            raise Exception("Error at line {%s}: invalid country coordinates" % line)

    country = {
        "name": args[0],
        "lowerLeft": {
            "x": int(args[1]),
            "y": int(args[2])
        },
        "upperRight": {
            "x": int(args[3]),
            "y": int(args[4])
        }
    }
    return country


def parse_input():
    cases = []

    lines = read_lines(data_folder)
    line_index = 0
    while line_index < len(lines):
        counties_len = int(lines[line_index])
        if counties_len == 0:
            return cases
        if counties_len > max_countries_amount or counties_len < 1:
            raise Exception("Error in input for case %i: invalid amount of countries" % (len(cases) + 1))
        line_index += 1

        countries_list = []
        for j in range(counties_len):
            parsed = parse_country(lines[line_index])
            countries_list.append(parsed)
            line_index += 1
        cases.append(countries_list)

    return cases
