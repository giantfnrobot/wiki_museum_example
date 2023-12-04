from museum_data_compiler import MuseumParser


if __name__ == "__main__":
    m = MuseumParser()
    museum_table = m.fetch_museum_data()
    m.dump_csv()
    print(museum_table)