# coding: utf-8
# license: GPLv3

import tkinter.filedialog
import solar_vis as vis
import solar_input
import solar_model as model


class Cosmos:
    def __init__(self):
        """Главная функция главного модуля.
        Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
        """

        self.perform_execution = False
        """Флаг цикличности выполнения расчёта"""

        self.space_objects = []
        """Список космических объектов."""

        print('Modelling started!')
        self.physical_time = 0
        """Физическое время от начала расчёта.
        Тип: float"""

        root = tkinter.Tk()
        # космическое пространство отображается на холсте типа Canvas
        self.space = tkinter.Canvas(root, width=vis.window_width, height=vis.window_height, bg="black")
        self.space.pack(side=tkinter.TOP)
        # нижняя панель с кнопками
        frame = tkinter.Frame(root)
        frame.pack(side=tkinter.BOTTOM)

        self.start_button = tkinter.Button(frame, text="Start", command=self.start_execution, width=6)
        self.start_button.pack(side=tkinter.LEFT)

        self.time_step = tkinter.DoubleVar()
        self.time_step.set(1)
        time_step_entry = tkinter.Entry(frame, textvariable=self.time_step)
        time_step_entry.pack(side=tkinter.LEFT)
        """Шаг по времени при моделировании.
        Тип: float"""

        self.time_speed = tkinter.DoubleVar()
        scale = tkinter.Scale(frame, variable=self.time_speed, orient=tkinter.HORIZONTAL, label="time speed")
        scale.pack(side=tkinter.LEFT)

        load_file_button = tkinter.Button(frame, text="Open file...", command=self.open_file_dialog)
        load_file_button.pack(side=tkinter.LEFT)
        save_file_button = tkinter.Button(frame, text="Save to file...", command=self.save_file_dialog)
        save_file_button.pack(side=tkinter.LEFT)

        self.displayed_time = tkinter.StringVar()
        self.displayed_time.set(str(self.physical_time) + " seconds gone")
        time_label = tkinter.Label(frame, textvariable=self.displayed_time, width=30)
        time_label.pack(side=tkinter.RIGHT)
        """Отображаемое на экране время.
        Тип: переменная tkinter"""

        self.space_writing = vis.update_system_name(self.space, "Space simulation")

        root.mainloop()
        print('Modelling finished!')

    def execution(self):
        """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
        а также обновляя их положение на экране.
        Цикличность выполнения зависит от значения глобальной переменной perform_execution.
        При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
        """
        model.recalculate_space_objects_positions(self.space_objects, self.time_step.get(), self.physical_time)
        for body in self.space_objects:
            vis.update_object_position(self.space, body)
        self.physical_time += self.time_step.get()
        self.displayed_time.set("%.1f" % self.physical_time + " seconds gone")

        if self.perform_execution:
            self.space.after(101 - int(self.time_speed.get()), self.execution)

    def start_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Запускает циклическое исполнение функции execution.
        """
        self.perform_execution = True
        self.start_button['text'] = "Pause"
        self.start_button['command'] = self.stop_execution

        self.execution()
        print('Started execution...')

    def stop_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Останавливает циклическое исполнение функции execution.
        """
        self.perform_execution = False
        self.start_button['text'] = "Start"
        self.start_button['command'] = self.start_execution
        print('Paused execution.')

    def open_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в глобальный список space_objects
        """
        self.perform_execution = False
        for obj in self.space_objects:
            self.space.delete(obj.image)  # удаление старых изображений планет
        in_filename = tkinter.filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
        self.space_objects = solar_input.read_space_objects_data_from_file(in_filename)
        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in self.space_objects])
        vis.calculate_scale_factor(max_distance)
        self.space_writing = vis.update_system_name(self.space, in_filename.split("/")[-1].split(".")[0],
                                                    self.space_writing)
        self.physical_time = 0

        for obj in self.space_objects:
            if obj.type == 'star':
                vis.create_star_image(self.space, obj)
            elif obj.type == 'planet':
                vis.create_planet_image(self.space, obj)
            else:
                raise AssertionError()

    def save_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и вызывает
        функцию считывания параметров системы небесных тел из данного файла.
        Считанные объекты сохраняются в глобальный список space_objects
        """
        time = self.physical_time
        out_filename = tkinter.filedialog.asksaveasfilename(filetypes=(("Text file", ".txt"),))
        solar_input.write_space_objects_data_to_file(out_filename, self.space_objects, time)


if __name__ == "__main__":
    c = Cosmos()
