# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
import matplotlib.pyplot as plt


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star" and len(line.split()) == 8:
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet" and len(line.split()) == 8:
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """

    star.R = float(line.split()[1])
    star.color = line.split()[2]
    star.m = float(line.split()[3])
    star.x = float(line.split()[4])
    star.y = float(line.split()[5])
    star.Vx = float(line.split()[6])
    star.Vy = float(line.split()[7])


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """

    planet.R = float(line.split()[1])
    planet.color = line.split()[2]
    planet.m = float(line.split()[3])
    planet.x = float(line.split()[4])
    planet.y = float(line.split()[5])
    planet.Vx = float(line.split()[6])
    planet.Vy = float(line.split()[7])


def write_space_objects_data_to_file(output_filename, space_objects, time):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    **time** — момент времени, в который произошло сохранение
    """
    speeds = []
    lengths = []
    times = []
    with open(output_filename, 'w') as out_file:
        count = 0
        print("Time:", time, "seconds", file=out_file)
        print("", file=out_file)
        for obj in space_objects:
            print(obj.type[0].upper() + obj.type[1::], obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy, file=out_file)
            print("", file=out_file)
            if count == 1:
                for i in range(len(obj.stats)):
                    speeds.append(obj.stats[i][0])
                    lengths.append(obj.stats[i][1])
                    times.append(obj.stats[i][2])
            count += 1  # графики считаются для второго поданного объекта относительно первого (предположительно Солнца)
        print(times)
        print(speeds)
        print(lengths)
        plt.plot(times, speeds, color="red")
        plt.grid()
        plt.xlabel("Time, s")
        plt.ylabel("Total velocity, m/s")
        plt.savefig("Grafic1.png")
        plt.clf()

        plt.plot(times, lengths, color="black")
        plt.grid()
        plt.xlabel("Time, s")
        plt.ylabel("Distance to sun, m")
        plt.savefig("Grafic2.png")
        plt.clf()

        plt.plot(lengths, speeds, color="blue")
        plt.grid()
        plt.xlabel("Distance to sun, m")
        plt.ylabel("Total velocity, m/s")
        plt.savefig("Grafic3.png")
        plt.clf()


if __name__ == "__main__":
    print("This module is not for direct call!")
