# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
        body.Fx += gravitational_constant * obj.m * body.m / r ** 3 * (obj.x - body.x)
        body.Fy += gravitational_constant * obj.m * body.m / r ** 3 * (obj.y - body.y)


def move_space_object(body, dt, t, sun):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    **dt** - величина малого промежутка времени, перемещение за которое рассматривается
    **t** - момент времени, в который происходит перемещение
    **sun** - 1я вводимый объект, предположительно солнце, для которого мыбудем считать расстояния
    """

    ax = body.Fx / body.m
    body.x += body.Vx * dt
    body.Vx += ax * dt
    ay = body.Fy / body.m
    body.y += body.Vy * dt
    body.Vy += ay * dt
    return [(body.Vx ** 2 + body.Vy ** 2) ** (1 / 2), ((sun.x - body.x) ** 2 + (sun.y - body.y) ** 2) ** (1 / 2), t]


def recalculate_space_objects_positions(space_objects, dt, t):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    **t** - момент времени
    """
    count = 0
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        if count == 1:
            new_stats = move_space_object(body, dt, t, space_objects[0])
        else:
            move_space_object(body, dt, t, space_objects[0])
        count += 1
    return new_stats


if __name__ == "__main__":
    print("This module is not for direct call!")
