from src import Map, parse_input


if __name__ == "__main__":
    cases = []
    try:
        cases = parse_input()
    except Exception as e:
        print(e)
        exit()

    for i, countries_list in enumerate(cases):
        print("\nCase Number %i" % (i + 1))

        try:
            europe_map = Map(countries_list)
            europe_map.simulate_euro_diffusion()
            for country in europe_map.countries:
                print(country.name, country.day_of_full)

        except Exception as e:
            print(e)
