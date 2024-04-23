import tkinter as tk
from tkinter import *
from tkinter import ttk

from matplotlib.figure import Figure
from PIL import Image, ImageTk
from model import Model


class App(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.title('Quality of Life')
        self.geometry("1920x1080")
        self.model = model
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill='both')
        self.current_frame = None
        self.set_frame(Home_Frame)

    def set_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame(self, self.frame)
        self.current_frame.pack(expand=True, fil='both')

    def run(self):
        self.mainloop()

    def exit(self):
        self.destroy()


class DemoFrame(tk.Frame):
    head_button = {'font': ('Century', 25, 'bold'), 'fg': '#a6a6a6', 'bg': '#f8f5ef', 'width': 8, 'bd': 0}

    def __init__(self, main_window, frame):
        super().__init__(frame)
        self.main = main_window

    def set_background(self, bg):
        # Create a canvas
        self.update()
        my_canvas = Canvas(self, width=self.main.winfo_width(), height=self.main.winfo_height())
        my_canvas.pack(fill="both", expand=True)

        # Set image in canvas
        my_canvas.create_image(0, 0, image=bg, anchor="nw")
        my_canvas.bg = bg

    def init_head_components(self):
        self.head_button['width'] = 8
        home_button = self.create_button('HOME', self.home_button_handler, self.head_button)
        home_button.place(x=20, y=30)

    def create_button(self, text: str, bind, opt):
        button = tk.Button(self, text=text, **opt)
        button.bind('<Button>', bind)
        return button

    def home_button_handler(self, *args):
        self.main.set_frame(Home_Frame)

    def button_handler(self, event, *args):
        frame_dict = {'Quality of Life Data': Data_Frame, 'Storytelling': Storytelling_Frame,
                      'Create Graph': Graph_Frame, 'Table Data': Data_Table, 'Data by Country': Data_Country,
                      'Descriptive Data': Data_Descriptive, 'Data Storytelling': Storytelling_Frame}
        key = event.widget['text']
        self.main.set_frame(frame_dict[key])


class Home_Frame(DemoFrame):
    button_opt = {'font': ('Ariel', 40, 'bold'), 'height': 1, 'bg': '#fac0d6'}

    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        img = PhotoImage(file='background/home.png')
        super().set_background(img)
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        exit_button = self.create_button('EXIT', self.exit_button_handler, self.head_button)
        exit_button.place(x=self.main.winfo_width()-200, y=30)

    def init_components(self):
        self.update()
        self.init_head_components()

    def exit_button_handler(self, *args):
        self.main.destroy()


class Data_Frame(DemoFrame):

    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        img = PhotoImage(file='background/data.png')
        self.set_background(img)
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        self.head_button['width'] = 12
        story_button = self.create_button('Storytelling', self.button_handler, self.head_button)
        story_button.place(x=self.main.winfo_width()-550, y=30)

        graph_button = self.create_button('Create Graph', self.button_handler, self.head_button)
        graph_button.place(x=self.main.winfo_width()-280, y=30)

    def init_components(self):
        self.init_head_components()


class Data_Table(DemoFrame):
    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        img = PhotoImage(file='background/data_table.png')
        self.set_background(img)
        self.sort = tk.StringVar()
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        self.head_button['width'] = 16
        data_button = self.create_button('Quality of Life Data', self.button_handler, self.head_button)
        data_button.place(x=210, y=30)

        self.head_button['width'] = 13
        country_button = self.create_button('Data by Country', self.button_handler, self.head_button)
        country_button.place(x=self.main.winfo_width() - 570, y=30)

        descriptive_button = self.create_button('Descriptive Data', self.button_handler, self.head_button)
        descriptive_button.place(x=self.main.winfo_width() - 290, y=30)

    def init_components(self):
        self.update()
        self.init_head_components()


class Data_Country(DemoFrame):
    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        img = PhotoImage(file='background/data_country.png')
        self.set_background(img)
        self.element = []
        self.country = tk.StringVar()
        self.transparent_image = Image.open('background/transparent.png')
        self.transparent_photo = ImageTk.PhotoImage(self.transparent_image)
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        self.head_button['width'] = 16
        data_button = self.create_button('Quality of Life Data', self.button_handler, self.head_button)
        data_button.place(x=210, y=30)

        self.head_button['width'] = 13
        table_button = self.create_button('Table Data', self.button_handler, self.head_button)
        table_button.place(x=self.main.winfo_width() - 570, y=30)

        descriptive_button = self.create_button('Descriptive Data', self.button_handler, self.head_button)
        descriptive_button.place(x=self.main.winfo_width() - 290, y=30)

    def init_components(self):
        self.init_head_components()


class Data_Descriptive(DemoFrame):
    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        img = PhotoImage(file='background/data_table.png')
        self.set_background(img)
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        self.head_button['width'] = 16
        data_button = self.create_button('Quality of Life Data', self.button_handler, self.head_button)
        data_button.place(x=210, y=30)

        self.head_button['width'] = 13
        table_button = self.create_button('Table Data', self.button_handler, self.head_button)
        table_button.place(x=self.main.winfo_width() - 570, y=30)

        country_button = self.create_button('Data by Country', self.button_handler, self.head_button)
        country_button.place(x=self.main.winfo_width() - 290, y=30)

    def init_components(self):
        self.init_head_components()


class Storytelling_Frame(DemoFrame):
    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        img = PhotoImage(file='background/data_country.png')
        self.set_background(img)
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        self.head_button['width'] = 16
        story_button = self.create_button('Quality of Life Data', self.button_handler, self.head_button)
        story_button.place(x=self.main.winfo_width() - 630, y=30)

        self.head_button['width'] = 12
        graph_button = self.create_button('Create Graph', self.button_handler, self.head_button)
        graph_button.place(x=self.main.winfo_width() - 280, y=30)

    def init_components(self):
        self.init_head_components()


class Graph_Frame(DemoFrame):

    def __init__(self, window_frame, frame):
        super().__init__(window_frame, frame)
        bg = PhotoImage(file='background/graph.png')
        self.set_background(bg)
        self.graph = tk.StringVar()
        self.init_components()

    def init_head_components(self):
        super().init_head_components()
        self.head_button['width'] = 16
        story_button = self.create_button('Quality of Life Data', self.button_handler, self.head_button)
        story_button.place(x=self.main.winfo_width()-630, y=30)

        self.head_button['width'] = 12
        graph_button = self.create_button('Storytelling', self.button_handler, self.head_button)
        graph_button.place(x=self.main.winfo_width()-280, y=30)

    def init_components(self):
        self.update()
        self.init_head_components()


if __name__ == '__main__':
    data = Model()
    app = App(data)
    app.run()
