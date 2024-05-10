"""Module for View Class"""
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View:
    """View Class for output section in Quality of Life App"""
    def __init__(self):
        self.data_tree = Data_Treeview
        self.data_country = Data_Country
        self.graph = Graph_View


class Data_Treeview(ttk.Treeview):
    """Treeview class represent the data in table form"""

    def __init__(self, root, columns):
        """Initialize the treeview"""
        super().__init__(root, columns=columns, show='headings', height=20)
        self.columns = columns
        self.set_heading()
        self.set_style()

    def set_heading(self):
        """Set the heading of  treeview"""
        width = [50, 160, 130, 160, 90, 120, 130, 190, 180, 100, 100, 180]
        for n in range(len(self.columns)):
            head = self.columns[n]
            self.heading(head, text=head)
            self.column(head, width=width[n], anchor=tk.W, stretch=tk.YES)

    def reset_data(self, data):
        """Reset the data in treeview
        :param data: new data for inserting into treeview"""
        self.remove_data()
        self.insert_data(data)

    def insert_data(self, data):
        """Insert new data into treeview
        :param data: new data for inserting into treeview
        """
        for n in range(len(data)):
            current_info = [str(data[column][n]) for column in self.columns]
            self.insert('', tk.END, values=current_info)

    def remove_data(self):
        """Remove all the data in treeview"""
        for row in self.get_children():
            self.delete(row)

    def set_style(self):
        """Set the style of the treeview"""
        style = ttk.Style(self)
        style.configure("Treeview", background="white",
                        fieldbackground="black", foreground="black")
        style.configure('Treeview.Heading', background="#76b9ff")
        style.configure('Treeview', rowheight=30)
        style.configure("Treeview", borderwidth=1, relief="solid")


class Data_Country(tk.Frame):
    colors = ['#fac0d6', '#f4a9c6', '#f898bd', '#76b9ff', '#5ba8f8', '#519be8', '#fdbc6b', '#f8ac4d', '#eb9e3d']

    def __init__(self, root, columns):
        super().__init__(root, bg='#f8f5ef')
        self.columns = columns
        self.init_components()

    def init_components(self):
        for h in range(9):
            label = self.create_index_frame(self.columns[h], self.colors[h])
            label.grid(row=h//3, column=h % 3, sticky=tk.NSEW, padx=4, pady=4)

        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

    def create_index_frame(self, head, color):
        """Create and return index frame contain head and value label for each index"""
        size = 17
        if len(head) > 20:
            size = 12
        frame = tk.Frame(self, bg=color, borderwidth=2, relief='solid')
        label_head = tk.Label(frame, text=head, font=('Ariel', size), bg=color)
        label_info = tk.Label(frame, text=' ', font=('Ariel', 35), bg=color)
        label_head.pack(side=tk.TOP, expand=True)
        label_info.pack(side=tk.TOP, expand=True)
        return frame

    def set_index(self, df):
        widget = self.winfo_children()
        for n in range(9):
            data = list(df[self.columns[n]])[0]
            head, info = widget[n].winfo_children()
            info.config(text=data)

    def set_rank(self, rank_list):
        widget = self.winfo_children()
        for n in range(9):
            head, info = widget[n].winfo_children()
            info.config(text=rank_list[n])


class Graph_View(FigureCanvasTkAgg):
    """Graph View class represent the graph in many types"""
    def __init__(self, root):
        """Initialize the graph using the FigureCanvasTkAgg"""
        self.fig = Figure(figsize=(7, 7), dpi=100, edgecolor='black', linewidth=2)
        super().__init__(self.fig, master=root)

    def clear_graph(self):
        """clear the current graph in figure"""
        self.fig.clear()

    def histogram(self, data, attribute, min_range, max_range):
        """Plot the Histogram Graph in figure
        :param data: data use to plot the graph
        :param attribute: the attribute of the histogram
        :param min_range: the minimum range of the attribute
        :param max_range: the maximum range of the attribute
        """
        plot = self.fig.add_subplot(1, 1, 1)
        plot.hist(data[attribute], bins=30, color='#76b9ff')

        plot.set_xlim(xmin=min_range, xmax=max_range)
        plot.set_xlabel(attribute)
        plot.set_ylabel('Number of Country')
        plot.set_title(f'{attribute} Histogram', fontsize=12, pad=20)

        self.draw()
        self.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def scatter(self, data, x_attribute: str, min_x, max_x, y_attribute: str, min_y, max_y):
        """Plot the scatter graph in figure
        :param data: data use to plot the graph
        :param x_attribute: the attribute on the x-axis
        :param min_x: the minimum range of the x-axis
        :param max_x: the maximum range of the x-axis
        :param y_attribute: the attribute on the y-axis
        :param min_y: the minimum range of the y-axis
        :param max_y: the maximum range of the y-axis
        """
        plot = self.fig.add_subplot(1, 1, 1)
        plot.scatter(data[x_attribute], data[y_attribute], color='#76b9ff')

        plot.set_xlim(xmin=min_x, xmax=max_x)
        plot.set_ylim(ymin=min_y, ymax=max_y)
        plot.set_xlabel(x_attribute)
        plot.set_ylabel(y_attribute)
        plot.set_title(f'Scatter Plot between {x_attribute} and {y_attribute}', fontsize=12, pad=20)

        self.draw()
        self.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def bar(self, data, x_attribute, y_attribute):
        """Plot Bar graph in figure
        :param data: data use to plot the graph
        :param x_attribute: the attribute on the x-axis
        :param y_attribute: the attribute on the y-axis
        """
        plot = self.fig.add_subplot(1, 1, 1)
        plot.bar(data.index, data, color='#76b9ff')

        if len(data.index) <= 8:
            for i, v in enumerate(data):
                plot.text(i, v + 0.1, f'{int(v):,}', ha='center', va='bottom')
        else:
            self.fig.subplots_adjust(bottom=0.2)
            plot.set_xticks(range(len(data.index)))
            plot.set_xticklabels(data.index, rotation=90, fontsize=6)

        plot.set_xlabel(x_attribute)
        plot.set_ylabel(y_attribute)
        plot.set_title(f'Bar Graph between {x_attribute} and {y_attribute}', fontsize=12, pad=20)

        self.draw()
        self.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def box_plot(self, data, attribute):
        """Plot Box Plot in figure
        :param data: data use to plot the graph
        :param attribute: attribute of the boxplot
        """
        plot = self.fig.add_subplot(1, 1, 1)
        box = plot.boxplot(data[attribute], patch_artist=True)
        box['boxes'][0].set(facecolor='#76b9ff')

        plot.set_ylabel(attribute)
        plot.set_title(f'{attribute} Boxplot', fontsize=12, pad=20)

        self.draw()
        self.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
