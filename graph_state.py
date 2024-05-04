"""Module for Graph State Class"""
import tkinter as tk
from tkinter import ttk


class Graph_state:
    """Frame for the input section, getting the components to create the graph"""

    font_option = {'font': ('Ariel', 16)}
    attribute_opt = {'side': tk.TOP, 'anchor': tk.W, 'fill': tk.X, 'pady': 20}
    button_opt = {'side': tk.LEFT, 'fill': tk.X, 'expand': True, 'padx': 5}

    def __init__(self, root, model, graph_view):
        """Initialize the Graph State class"""
        self.root = root
        self.model = model
        self.graph_view = graph_view
        self.attribute_frame = tk.Frame(root, bg='#f8f5ef', borderwidth=1, relief='solid')
        self.attribute_frame.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=100, fill=tk.X)

    def init_graph_components(self):
        """Initialize the components for plotting the graph"""
        pass

    def combo_label_frame(self, text, variable, values, current=0):
        """Create and return frame contain the name label and combobox"""
        frame = tk.Frame(self.attribute_frame, bg='#f8f5ef')
        label = tk.Label(frame, text=text, **self.font_option, bg='#f8f5ef')
        label.pack(side=tk.LEFT, fill=tk.X, anchor=tk.NW, padx=10)

        select = ttk.Combobox(frame, textvariable=variable, state='readonly', **self.font_option)
        select['values'] = values
        select.current(newindex=current)
        select.bind('<<ComboboxSelected>>', self.update_graph)
        select.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)
        return frame

    def range_frame(self, text, min_var, max_var, state='normal', entry_list=None):
        """Create and return frame contain min and max label and entry"""
        frame = tk.Frame(self.attribute_frame, bg='#f8f5ef')
        range_label = tk.Label(frame, text=text, **self.font_option, bg='#f8f5ef')
        range_label.pack(side=tk.LEFT, padx=10)

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
        range_frame.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)

        return frame

    def button_frame(self):
        """Create and return frame contain set and reset range button"""
        button_frame = tk.Frame(self.attribute_frame, bg='#f8f5ef')
        set_button = tk.Button(button_frame, text='Set Range', **self.font_option, bg='#fac0d6')
        set_button.bind('<Button>', self.update_graph)
        set_button.pack(**self.button_opt)

        reset_button = tk.Button(button_frame, text='Reset Range', **self.font_option, bg='#fac0d6')
        reset_button.bind('<Button>', self.reset_range)
        reset_button.pack(**self.button_opt)
        button_frame.pack(**self.attribute_opt, padx=10)
        return button_frame

    def check_entry_input(self, entry):
        """Check and translate the entry input"""
        try:
            entry_input = float(entry.get())
        except ValueError:
            entry_input = None
            entry.set('')
        return entry_input

    def reset_range(self, *args):
        """Clear the range entry and plot the graph with original range"""
        pass

    def update_graph(self, *args):
        """Update the graph with new type or new component"""
        pass

    def show_graph(self):
        """display the graph on the screen"""
        pass


class Histogram(Graph_state):
    """Frame contain the input section for Histogram graph components"""

    def __init__(self, root, model, graph_view):
        """Initialize the attribute in the frame"""
        super().__init__(root, model, graph_view)
        self.attribute = tk.StringVar()
        self.min = tk.StringVar()
        self.max = tk.StringVar()
        self.entry_list = []
        self.init_graph_components()

    def init_graph_components(self):
        """Initialize the components in the frame"""
        attribute = self.combo_label_frame('Attribute', self.attribute, self.model.columns()[2:])
        attribute.pack(**self.attribute_opt)

        self.range = self.range_frame('Range', self.min, self.max, 'readonly', self.entry_list)
        self.range.pack(**self.attribute_opt)

        button_frame = self.button_frame()
        button_frame.pack(**self.attribute_opt, padx=10)

        self.show_graph()

    def reset_range(self, event, *args):
        """Clear range entry and replot the graph"""
        self.min.set('')
        self.max.set('')
        self.update_graph(event)

    def change_entry_state(self, state):
        """Change the entry state"""
        for widget in self.entry_list:
            widget['state'] = state

    def update_graph(self, event, *args):
        """Change the graph type"""
        event.widget.selection_clear()

        if isinstance(event.widget, ttk.Combobox):
            self.min.set('')
            self.max.set('')
            self.change_entry_state('normal')
            if self.attribute.get() == 'Continent':
                self.change_entry_state('disabled')

        self.show_graph()

    def show_graph(self):
        """Clear current graph and plot new histogram"""
        attribute = self.attribute.get()
        min_range = self.check_entry_input(self.min)
        max_range = self.check_entry_input(self.max)

        self.graph_view.clear_graph()
        self.graph_view.histogram(self.model.data, attribute, min_range, max_range)


class Scatter_Plot(Graph_state):
    """Frame contain the input section for Scatter graph components"""

    def __init__(self, root, model, graph_view):
        """Initialize the frame and some variable"""
        super().__init__(root, model, graph_view)
        self.x = tk.StringVar()
        self.min_x = tk.StringVar()
        self.max_x = tk.StringVar()
        self.y = tk.StringVar()
        self.min_y = tk.StringVar()
        self.max_y = tk.StringVar()
        self.init_graph_components()

    def init_graph_components(self):
        """Initialize the components in the frame"""
        x_attribute = self.combo_label_frame('x-attribute', self.x, self.model.index_columns())
        x_range = self.range_frame('Range', self.min_x, self.max_x)
        y_attribute = self.combo_label_frame('y-attribute', self.y, self.model.index_columns(), 1)
        y_range = self.range_frame('Range', self.min_y, self.max_y)
        x_attribute.pack(**self.attribute_opt)
        x_range.pack(**self.attribute_opt)
        y_attribute.pack(**self.attribute_opt)
        y_range.pack(**self.attribute_opt)

        button_frame = self.button_frame()
        button_frame.pack(**self.attribute_opt, padx=10)

        self.show_graph()
        self.attribute_frame.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=100, fill=tk.X)

    def reset_range(self, event, *args):
        """Clear all the range entry and replot the graph with the original range"""
        self.min_x.set('')
        self.max_x.set('')
        self.min_y.set('')
        self.max_y.set('')
        self.update_graph(event)

    def update_graph(self, event, *args):
        """Clear the input section and plot the graph"""
        event.widget.selection_clear()
        self.show_graph()

    def show_graph(self):
        """Plot scatter with the input attribute"""
        x = self.x.get()
        min_x = self.check_entry_input(self.min_x)
        max_x = self.check_entry_input(self.max_x)

        y = self.y.get()
        min_y = self.check_entry_input(self.min_y)
        max_y = self.check_entry_input(self.max_y)

        self.graph_view.clear_graph()
        self.graph_view.scatter(self.model.data, x, min_x, max_x, y, min_y, max_y)


class Bar_Graph(Graph_state):
    """Frame contain the input section for Bar graph components"""

    def __init__(self, root, model, graph_view):
        """Initialize the frame and some variable"""
        super().__init__(root, model, graph_view)
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.min_y = tk.StringVar()
        self.max_y = tk.StringVar()
        self.init_graph_components()

    def init_graph_components(self):
        """Initialize components in the frame"""
        x_attribute = self.combo_label_frame('x-attribute', self.x, ['Country', 'Continent'], 1)
        y_attribute = self.combo_label_frame('y-attribute', self.y, self.model.numerical_columns())
        y_range = self.range_frame('Range', self.min_y, self.max_y)
        x_attribute.pack(**self.attribute_opt)
        y_attribute.pack(**self.attribute_opt)
        y_range.pack(**self.attribute_opt)

        button_frame = self.button_frame()
        button_frame.pack(**self.attribute_opt, padx=10)

        self.show_graph()
        self.attribute_frame.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=100, fill=tk.X)

    def reset_range(self, event, *args):
        """Clear the entry range and plot graph with original range"""
        self.min_y.set('')
        self.max_y.set('')
        self.update_graph(event)

    def update_graph(self, event, *args):
        """Clear the selection and display the graph"""
        event.widget.selection_clear()
        self.show_graph()

    def show_graph(self):
        """Clear current graph and plot new scatter plot"""
        x = self.x.get()

        y = self.y.get()
        min_y = self.check_entry_input(self.min_y)
        max_y = self.check_entry_input(self.max_y)

        data = self.model.group_data(by=x, attribute=y)
        data = self.model.filter_range_data(min_y, max_y, data)

        self.graph_view.clear_graph()
        self.graph_view.bar(data, x, y)


class Box_Plot(Graph_state):
    """Frame contain the input section for Box plot graph components"""

    def __init__(self, root, model, graph_view):
        """Initialize the frame and some variable"""
        super().__init__(root, model, graph_view)
        self.attribute = tk.StringVar()
        self.entry_list = []
        self.attribute_frame.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=100, fill=tk.X)
        self.init_graph_components()

    def init_graph_components(self):
        """Initialize the components in the frame"""
        attribute = self.combo_label_frame('Attribute', self.attribute, self.model.numerical_columns())
        attribute.pack(**self.attribute_opt)

        self.show_graph()

    def update_graph(self, event, *args):
        """Clear the input selection and plot new graph"""
        event.widget.selection_clear()
        self.show_graph()

    def show_graph(self):
        """Plot Box plot with input attribute"""
        attribute = self.attribute.get()
        self.graph_view.clear_graph()
        self.graph_view.box_plot(self.model.data, attribute)
