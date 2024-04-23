import tkinter as tk
from view import Graph_View
from tkinter import ttk


class Graph:
    font_option = {'font': ('Ariel', 16)}

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.graph_view = Graph_View(model.data)
        self.graph_canvas = None
        self.children = []

    def init_graph_components(self):
        pass

    def combo_label_frame(self, text, variable, values, current=0):
        frame = tk.Frame(self.root, bg='#f8f5ef')
        label = tk.Label(frame, text=text, **self.font_option, bg='#f8f5ef')
        label.pack(side=tk.LEFT)

        select = ttk.Combobox(frame, width=27, textvariable=variable, state='readonly', **self.font_option)
        select['values'] = values
        select.current(newindex=current)
        select.bind('<<ComboboxSelected>>', self.update_graph)
        select.pack(side=tk.LEFT, padx=10)
        return frame

    def range_frame(self, text, min_var, max_var, state='normal', entry_list=None):
        frame = tk.Frame(self.root, bg='#f8f5ef')
        range_label = tk.Label(frame, text=text, **self.font_option, bg='#f8f5ef')
        range_label.pack(side=tk.LEFT)

        range_frame = tk.Frame(frame, width=150, height=80, bg='#f8f5ef', borderwidth=3, relief='groove')
        min_label = tk.Label(range_frame, text='min', **self.font_option, bg='#f8f5ef')
        min_entry = tk.Entry(range_frame, textvariable=min_var, width=10, state=state, **self.font_option)
        min_entry.bind('<Return>', self.update_graph)

        max_label = tk.Label(range_frame, text='max', **self.font_option, bg='#f8f5ef')
        max_entry = tk.Entry(range_frame, textvariable=max_var, width=10, state=state, **self.font_option)
        max_entry.bind('<Return>', self.update_graph)

        if entry_list is not None:
            entry_list.append(min_entry)
            entry_list.append(max_entry)

        pack_option = {'side': tk.LEFT, 'expand': True, 'fill': tk.BOTH, 'padx': 10, 'pady': 10}
        min_label.pack(**pack_option)
        min_entry.pack(**pack_option)
        max_label.pack(**pack_option)
        max_entry.pack(**pack_option)
        range_frame.pack(side=tk.LEFT, padx=20)

        return frame

    def check_entry_input(self, entry):
        try:
            entry_input = float(entry.get())
        except ValueError:
            entry_input = None
            entry.set('')
        return entry_input

    def update_graph(self, *args):
        pass

    def show_graph(self):
        pass


class Histogram(Graph):
    def __init__(self, root, model):
        super().__init__(root, model)
        self.attribute = tk.StringVar()
        self.min = tk.StringVar()
        self.max = tk.StringVar()
        self.entry_list = []
        self.init_graph_components()

    def init_graph_components(self):
        dis_x = self.root.main.winfo_width() * 4 / 6
        dis_y = self.root.main.winfo_height() / 4

        attribute = self.combo_label_frame('Attribute', self.attribute, self.model.columns()[2:])
        attribute.place(x=dis_x, y=dis_y)
        self.children.append(attribute)

        self.range = self.range_frame('Range', self.min, self.max, 'readonly', self.entry_list)
        self.range.place(x=dis_x, y=dis_y+80)
        self.children.append(self.range)

        reset_button = tk.Button(self.root, text='Reset Range', **self.font_option, bg='#fac0d6', width=20)
        reset_button.bind('<Button>', self.reset_range)
        reset_button.place(x=dis_x, y=dis_y + 200)
        self.children.append(reset_button)

        self.show_graph()

    def reset_range(self, event, *args):
        self.min.set('')
        self.max.set('')
        self.update_graph(event)

    def change_entry_state(self, state):
        for widget in self.entry_list:
            widget['state'] = state

    def update_graph(self, event, *args):
        event.widget.selection_clear()

        if isinstance(event.widget, ttk.Combobox):
            self.min.set('')
            self.max.set('')
            self.change_entry_state('normal')
            if self.attribute.get() == 'Continent':
                self.change_entry_state('disabled')

        self.show_graph()

    def show_graph(self):
        attribute = self.attribute.get()
        min_range = self.check_entry_input(self.min)
        max_range = self.check_entry_input(self.max)

        graph_canvas = self.graph_view.histogram(self.root, attribute, min_range, max_range)
        graph_canvas.get_tk_widget().place(x=150, y=250)
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()
        self.graph_canvas = graph_canvas
        self.children.append(self.graph_canvas)


class Scatter_Plot(Graph):
    def __init__(self, root, model):
        super().__init__(root, model)
        self.x = tk.StringVar()
        self.min_x = tk.StringVar()
        self.max_x = tk.StringVar()
        self.y = tk.StringVar()
        self.min_y = tk.StringVar()
        self.max_y = tk.StringVar()
        self.init_graph_components()

    def init_graph_components(self):
        dis_x = self.root.main.winfo_width() * 4 / 6
        dis_y = self.root.main.winfo_height() / 4 + 20

        x_attribute = self.combo_label_frame('x-attribute', self.x, self.model.index_columns())
        x_attribute.place(x=dis_x, y=dis_y)
        self.children.append(x_attribute)
        x_range = self.range_frame('Range', self.min_x, self.max_x)
        x_range.place(x=dis_x, y=dis_y+80)
        self.children.append(x_range)

        y_attribute = self.combo_label_frame('y-attribute', self.y, self.model.index_columns(), 1)
        y_attribute.place(x=dis_x, y=dis_y+220)
        self.children.append(y_attribute)
        y_range = self.range_frame('Range', self.min_y, self.max_y)
        y_range.place(x=dis_x, y=dis_y + 300)
        self.children.append(y_range)

        reset_button = tk.Button(self.root, text='Reset Range', **self.font_option, bg='#fac0d6', width=20)
        reset_button.bind('<Button>', self.reset_range)
        reset_button.place(x=dis_x, y=dis_y+420)
        self.children.append(reset_button)

        self.show_graph()

    def reset_range(self, event, *args):
        self.min_x.set('')
        self.max_x.set('')
        self.min_y.set('')
        self.max_y.set('')
        self.update_graph(event)

    def update_graph(self, event, *args):
        event.widget.selection_clear()
        self.show_graph()

    def show_graph(self):
        x = self.x.get()
        min_x = self.check_entry_input(self.min_x)
        max_x = self.check_entry_input(self.max_x)

        y = self.y.get()
        min_y = self.check_entry_input(self.min_y)
        max_y = self.check_entry_input(self.max_y)

        graph_canvas = self.graph_view.scatter(self.root, x, min_x, max_x, y, min_y, max_y)
        graph_canvas.get_tk_widget().place(x=150, y=250)

        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()
        self.graph_canvas = graph_canvas
        self.children.append(self.graph_canvas)


class Bar_Graph(Graph):
    def __init__(self, root, model):
        super().__init__(root, model)
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.min_y = tk.StringVar()
        self.max_y = tk.StringVar()
        self.init_graph_components()

    def init_graph_components(self):
        dis_x = self.root.main.winfo_width() * 4 / 6
        dis_y = self.root.main.winfo_height() / 4 + 20

        x_attribute = self.combo_label_frame('x-attribute', self.x, ['Country', 'Continent'], 1)
        x_attribute.place(x=dis_x, y=dis_y)
        self.children.append(x_attribute)

        y_attribute = self.combo_label_frame('y-attribute', self.y, self.model.numerical_columns())
        y_attribute.place(x=dis_x, y=dis_y+100)
        self.children.append(y_attribute)
        y_range = self.range_frame('Range', self.min_y, self.max_y)
        y_range.place(x=dis_x, y=dis_y + 160)
        self.children.append(y_range)

        reset_button = tk.Button(self.root, text='Reset Range', **self.font_option, bg='#fac0d6', width=20)
        reset_button.bind('<Button>', self.reset_range)
        reset_button.place(x=dis_x, y=dis_y+300)
        self.children.append(reset_button)

        self.show_graph()

    def reset_range(self, event, *args):
        self.min_y.set('')
        self.max_y.set('')
        self.update_graph(event)

    def update_graph(self, event, *args):
        event.widget.selection_clear()
        self.show_graph()

    def show_graph(self):
        x = self.x.get()

        y = self.y.get()
        min_y = self.check_entry_input(self.min_y)
        max_y = self.check_entry_input(self.max_y)

        data = self.model.group_data(by=x, attribute=y)
        data = self.model.filter_range_data(min_y, max_y, data)

        graph_canvas = self.graph_view.bar(self.root, data, x, y, min_y, max_y)
        graph_canvas.get_tk_widget().place(x=150, y=250)

        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()
        self.graph_canvas = graph_canvas
        self.children.append(self.graph_canvas)


class Box_Plot(Graph):
    def __init__(self, root, model):
        super().__init__(root, model)
        self.attribute = tk.StringVar()
        self.entry_list = []
        self.init_graph_components()

    def init_graph_components(self):
        dis_x = self.root.main.winfo_width() * 4 / 6
        dis_y = self.root.main.winfo_height() / 4

        attribute = self.combo_label_frame('Attribute', self.attribute, self.model.numerical_columns())
        attribute.place(x=dis_x, y=dis_y)
        self.children.append(attribute)

        self.show_graph()

    def update_graph(self, event, *args):
        event.widget.selection_clear()
        self.show_graph()

    def show_graph(self):
        attribute = self.attribute.get()

        graph_canvas = self.graph_view.box_plot(self.root, attribute)
        graph_canvas.get_tk_widget().place(x=150, y=250)
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()
        self.graph_canvas = graph_canvas
        self.children.append(self.graph_canvas)




