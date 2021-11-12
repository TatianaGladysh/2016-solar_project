# coding: utf-8
# license: GPLv3

import tkinter.filedialog
import solar_vis as vis
import solar_input
import solar_model as model


class Cosmos:
    def __init__(self):
        """
        Главная функция главного модуля.
        Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
        """

        self.have_model = False
        """Есть ли сейчас загруженная модель"""

        self.perform_execution = False
        """Флаг цикличности выполнения расчёта"""

        self.space_objects = []
        """Список космических объектов."""

        print('Modelling started!')
        self.physical_time = 0
        """Физическое время от начала расчёта.
        Тип: float"""

        self.stats = []
        """Хранение данных для графиков"""

        # космическое пространство отображается на холсте типа Canvas
        self.space = tkinter.Canvas(root, width=vis.window_width, height=vis.window_height, bg="black")
        self.space.pack(side=tkinter.TOP)
        # нижняя панель с кнопками
        frame = tkinter.Frame(root)
        frame.pack(side=tkinter.BOTTOM)

        self.start_button = tkinter.Button(frame, text="Start", command=self.start_execution, width=6)
        self.start_button.pack(side=tkinter.LEFT)

        self.time_step = tkinter.StringVar()
        self.time_step.set(1)
        time_step_entry = tkinter.Entry(frame, textvariable=self.time_step)
        time_step_entry.pack(side=tkinter.LEFT)
        """Шаг по времени при моделировании.
        Тип: float"""
        self.last_correct_time_step = 1
        """Последнее корректное введенное в окно значение"""

        self.time_speed = tkinter.DoubleVar()
        scale = tkinter.Scale(frame, variable=self.time_speed, orient=tkinter.HORIZONTAL, label="time speed")
        scale.pack(side=tkinter.LEFT)
        """Шкала с ползунком для увеличения скорости обработки заданных в окошке шагов времени"""

        load_file_button = tkinter.Button(frame, text="Open file...", command=self.open_file_dialog)
        load_file_button.pack(side=tkinter.LEFT)
        save_file_button = tkinter.Button(frame, text="Save to file...", command=self.save_file_dialog)
        save_file_button.pack(side=tkinter.LEFT)
        """Кнопки открытия новой модели и сохранения текущих значений модели в файл с одновременным созданием графиков
        движения для самой ближней к Солнцу планеты"""

        self.displayed_time = tkinter.StringVar()
        self.displayed_time.set(str(self.physical_time) + " seconds gone")
        time_label = tkinter.Label(frame, textvariable=self.displayed_time, width=30)
        time_label.pack(side=tkinter.RIGHT)
        """Отображаемое на экране время.
        Тип: переменная tkinter"""

        self.space_writing = vis.update_system_name(self.space, "Space simulation")
        """Название модели"""

        self.scale_factor = None
        """Масштабирование экранных координат по отношению к физическим.
        Тип: float
        Мера: количество пикселей на один метр."""

        print('Modelling finished!')

    def execution(self):
        """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
        а также обновляя их положение на экране.
        Цикличность выполнения зависит от значения глобальной переменной perform_execution.
        При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
        При некорректном введенном в окно значении, которое нельзя интерпретировать как число, выдается ошибка и
        для пересчета используется последнее корректное значение.
        """
        if self.perform_execution:
            fixed_time_step = self.time_step.get()
            if fixed_time_step != "" and fixed_time_step.isnumeric():
                self.last_correct_time_step = float(fixed_time_step)
            else:
                print('Wrong data format')
                self.time_step.set(self.last_correct_time_step)
            if self.have_model:
                self.stats.append(
                    model.recalculate_space_objects_positions(self.space_objects, self.last_correct_time_step,
                                                              self.physical_time))
            for body in self.space_objects:
                vis.update_object_position(self.space, body, self.scale_factor)
            self.physical_time += self.last_correct_time_step
            self.displayed_time.set("%.1f" % self.physical_time + " seconds gone")
            root.update()
            self.space.after(101 - int(self.last_correct_time_step), self.execution)

    def start_execution(self):
        """Обработчик события нажатия на кнопку Start.
        Запускает циклическое исполнение функции execution, если есть открытая модель.
        """
        if not self.have_model:
            print('You should open model')
            return
        self.perform_execution = True
        self.start_button['text'] = "Pause"
        self.start_button['command'] = self.stop_execution
        root.update()

        self.execution()
        print('Started execution...')
        # if self.time_step.get() != "" and self.time_step.get().isnumeric():
        #
        # else:
        #     print('Wrong data format')

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
        self.stop_execution()
        in_filename = tkinter.filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
        if in_filename != '':
            self.have_model = True
            for i in range(len(self.space_objects)):
                self.space.delete(self.space_objects[-1].image)  # удаление старых изображений планет
                self.space_objects.pop()
            self.space_objects = solar_input.read_space_objects_data_from_file(in_filename)
            max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in self.space_objects])
            self.scale_factor = vis.calculate_scale_factor(max_distance)
            self.space_writing = vis.update_system_name(self.space, in_filename.split("/")[-1].split(".")[0],
                                                        self.space_writing)
            self.stats = []
            self.physical_time = 0
            self.displayed_time.set(str(self.physical_time) + " seconds gone")

            for obj in self.space_objects:
                if obj.type == 'star':
                    vis.create_star_image(self.space, obj, self.scale_factor)
                elif obj.type == 'planet':
                    vis.create_planet_image(self.space, obj, self.scale_factor)
                else:
                    raise AssertionError()

    def save_file_dialog(self):
        """Открывает диалоговое окно выбора имени файла и сохранияет статистику в выбранный файл.
        Создает 3 файла с графиками зависимостей параметров первой от звезды планеты
        Выходит, если еще нет открытой модели
        """
        if not self.have_model:
            print('You should open model')
            return
        self.stop_execution()
        out_filename = tkinter.filedialog.asksaveasfilename(filetypes=(("Text file", ".txt"),))
        if out_filename != '':
            solar_input.write_space_objects_data_to_file(out_filename, self.space_objects, self.physical_time)
            solar_input.made_graphics(self.stats)


if __name__ == "__main__":
    root = tkinter.Tk()
    cosmos = Cosmos()
    root.mainloop()
