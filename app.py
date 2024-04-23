import tkinter as tk
from tkinter import *

from matplotlib.figure import Figure

from view import Data_Treeview, Graph_View
from tkinter import ttk
from PIL import Image, ImageTk
from model import Model
from graph import Histogram, Scatter_Plot, Bar_Graph, Box_Plot


class App(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.title('flight between cities in asia')
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
        width = int(self.main.winfo_width() / 100)
        self.button_opt['width'] = width

        data_button = self.create_button('Quality of Life Data', self.button_handler, self.button_opt)
        story_button = self.create_button('Data Storytelling', self.button_handler, self.button_opt)
        graph_button = self.create_button('Create Graph', self.button_handler, self.button_opt)

        dis_x = self.main.winfo_width() * 7/11
        dis_y = self.main.winfo_height() * 2/7 + 30
        data_button.place(x=dis_x, y=dis_y)
        story_button.place(x=dis_x, y=dis_y+150)
        graph_button.place(x=dis_x, y=dis_y+300)

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
        button_option = {'font': ('Ariel', 35, 'bold'), 'width': 15,
                         'height': 1, 'bg': '#fac0d6'}

        dis_y = self.main.winfo_height()*7/9
        dis_x = self.main.winfo_width()/2 - 150
        table_button = tk.Button(self, text='Table Data', **button_option)
        table_button.bind('<Button>', self.button_handler)
        table_button.place(x=dis_x-580, y=dis_y)

        country_button = tk.Button(self, text='Data by Country', **button_option)
        country_button.bind('<Button>', self.button_handler)
        country_button.place(x=dis_x, y=dis_y)

        descriptive_button = tk.Button(self, text='Descriptive Data', **button_option)
        descriptive_button.bind('<Button>', self.button_handler)
        descriptive_button.place(x=dis_x+580, y=dis_y)


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

        font_option = {'font': ('Ariel', 16)}

        box_y = self.main.winfo_height() / 7 + 10
        sort_label = tk.Label(self, text='Sort by', **font_option, bg='#f8f5ef')
        sort_label.place(x=700, y=box_y)

        sort_by = ttk.Combobox(self, width=27, textvariable=self.sort, **font_option, state='readonly')
        sort_by['values'] = self.main.model.index_columns()
        sort_by.current(newindex=0)
        sort_by.bind("<<ComboboxSelected>>", self.sort_tree)
        sort_by.place(x=800, y=box_y)

        self.info_label = tk.Label(self, text='(Higher is Better)', **font_option, fg='DodgerBlue4', bg='#f8f5ef')
        self.info_label.place(x=1200, y=box_y)

        self.tree = self.init_treeview()
        tree_y = self.main.winfo_height()/4
        self.tree.place(x=120, y=tree_y)
        self.tree.reset_data(self.main.model.data)

    def init_treeview(self):
        columns = list(self.main.model.columns())
        columns.remove('Continent')
        columns.remove('Population')
        columns.remove('Area')
        columns.remove('Density')
        tree = Data_Treeview(self, columns)
        return tree

    def sort_tree(self, event, *args):
        event.widget.selection_clear()
        sort_by = self.sort.get()
        sort_data = self.main.model.sort_data(sort_by)
        self.tree.reset_data(sort_data)

        info = '(Higher is Better)'
        if sort_by in self.main.model.lower_value():
            info = '(Lower is Better)'
        self.info_label.config(text=info)


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
        font_option = {'font': ('Ariel', 16)}

        dis_y = self.main.winfo_height() / 7 + 10
        country_label = tk.Label(self, text='Country', **font_option, bg='#f8f5ef')
        country_label.place(x=700, y=dis_y)

        self.select_country = ttk.Combobox(self, width=27, textvariable=self.country,
                                      state='readonly', **font_option)
        self.select_country['values'] = self.main.model.country_name()
        self.select_country.current(newindex=0)
        self.select_country.bind('<<ComboboxSelected>>', self.set_data)
        self.select_country.place(x=800, y=dis_y)

        self.set_data()

    def set_data(self, *args):
        self.select_country.selection_clear()

        element = self.element.copy()
        self.element = []

        country = self.country.get()
        country_data = self.main.model.filter_data({'Country': country})

        title_frame = self.title_frame(country, list(country_data["Continent"])[0])
        title_frame.place(x=150, y=290)
        self.element.append(title_frame)

        self.create_label(list(country_data["Rank"])[0], x=310, y=770, size=70)
        self.create_label(list(country_data["Quality of Life Index"])[0], x=755, y=805, size=40)

        self.create_label(f'{list(country_data["Area"])[0]:,} kilometer per square', x=350, y=435, size=20)
        self.create_label(f'{list(country_data["Population"])[0]:,}', x=405, y=508, size=20)
        self.create_label(list(country_data["Density"])[0], x=370, y=590, size=20)

        col = self.main.model.index_columns()
        self.index_frame(country_data, [col[1], col[4], col[7]], ['#d53e4f', '#c6e792', '#abdda4'], 1045)
        self.index_frame(country_data, [col[2], col[5], col[8]], ['#f46d43', '#e6f598', '#66c2a5'], 1305)
        self.index_frame(country_data, [col[3], col[6], col[9]], ['#fdae61', '#ffffbf', '#3288bd'], 1565)

        for widget in element:
            widget.destroy()

    def index_frame(self, df, column, color, x):
        height = [350, 580, 810]
        for h in range(len(height)):
            label = tk.Label(self, text=list(df[column[h]])[0], font=('Ariel', 40), bg=color[h],
                             width=5, anchor=tk.CENTER)
            label.place(x=x, y=height[h])

    def title_frame(self, country, continent):
        frame = tk.Frame(self, bg='#f8f5ef')
        country = tk.Label(frame, text=country, font=('Ariel', 40), bg='#f8f5ef')
        continent = tk.Label(frame, text=f'({continent})', font=('Ariel', 20), bg='#f8f5ef')
        country.pack(side=tk.LEFT)
        continent.pack(side=tk.LEFT, padx=40)
        return frame

    def create_label(self, text, x, y, size=16):
        label = tk.Label(self, text=text, font=('Ariel', int(size)), bg='#f8f5ef')
        label.place(x=x, y=y)
        self.element.append(label)


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
    graph_class = {'Histogram': Histogram, 'Scatter': Scatter_Plot, 'Bar Graph': Bar_Graph, 'Box Plot': Box_Plot}

    def __init__(self, window_frame, frame):
        super().__init__(window_frame, frame)
        bg = PhotoImage(file='background/graph.png')
        self.set_background(bg)
        self.graph = tk.StringVar()
        self.state = Histogram
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
        font_option = {'font': ('Ariel', 16)}
        dis_y = self.main.winfo_height() / 7 + 10
        type_label = tk.Label(self, text='Type', **font_option, bg='#f8f5ef')
        type_label.place(x=520, y=dis_y)

        select_graph = ttk.Combobox(self, width=27, textvariable=self.graph,
                                    state='readonly', **font_option)
        select_graph['values'] = ['Histogram', 'Scatter', 'Bar Graph', 'Box Plot']
        select_graph.current(newindex=0)
        select_graph.bind('<<ComboboxSelected>>', self.change_type)
        select_graph.place(x=600, y=160)

        self.current_graph = self.state(self, self.main.model)

    def change_type(self, event, *args):
        event.widget.selection_clear()
        for widget in self.current_graph.children:
            try:
                widget.destroy()
            except AttributeError:
                widget.get_tk_widget().destroy()
        self.state = self.graph_class[self.graph.get()]
        self.current_graph = self.state(self, self.main.model)


if __name__ == '__main__':
    data = Model()
    app = App(data)
    app.run()
