# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 800
"""Ширина окна"""

window_height = 600
"""Высота окна"""


def calculate_scale_factor(max_distance):
    """
    Вычисляет значение переменной масштабирования по данной характерной длине
    Возвращает переменную масштабирования

    Параметры:

    **max_distance** — максимальное расстояние до одной из планет.
    """
    scale_factor_to_calculate = 0.3 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor_to_calculate)
    return scale_factor_to_calculate


def scale_x(x, scale_factor):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    **scale_factor** - коэффициент масштабирования.
    """

    return int(x * scale_factor) + window_width // 2


def scale_y(y, scale_factor):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    **scale_factor** - коэффициент масштабирования.
    """

    return int(window_height / 2 - y * scale_factor)


def create_star_image(space, star, scale_factor):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    **scale_factor** - коэффициент масштабирования.
    """

    x = scale_x(star.x, scale_factor)
    y = scale_y(star.y, scale_factor)
    r = star.R
    star.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=star.color)


def create_planet_image(space, planet, scale_factor):
    """Создаёт отображаемый объект планеты.

    Параметры:

    **space** — холст для рисования.
    **planet** — объект планеты.
    **scale_factor** - коэффициент масштабирования.
    """
    x = scale_x(planet.x, scale_factor)
    y = scale_y(planet.y, scale_factor)
    r = planet.R
    planet.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=planet.color)


def update_system_name(space, system_name, space_writing=0):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    **space_writing** - написанный на холсте текст
    """
    if space_writing != 0:
        space.delete(space_writing)
    return space.create_text(window_width / 2, 20, tag="header", text=system_name, font=header_font, fill="magenta")


def update_object_position(space, body, scale_factor):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    **scale_factor** - коэффициент масштабирования.
    """
    x = scale_x(body.x, scale_factor)
    y = scale_y(body.y, scale_factor)
    r = body.R
    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(body.image, window_width + r, window_height + r,
                     window_width + 2 * r, window_height + 2 * r)  # положить за пределы окна
    space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")
