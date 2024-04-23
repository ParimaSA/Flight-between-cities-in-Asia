from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Data_Treeview(ttk.Treeview):
    def __init__(self, root, columns):
        super().__init__(root, columns=columns, show='headings', height=20)
        self.columns = columns
        self.set_heading()
        self.set_style()

    def set_heading(self):
        width = [50, 170, 130, 160, 90, 120, 130, 190, 190, 100, 100, 180]
        for n in range(len(self.columns)):
            head = self.columns[n]
            self.heading(head, text=head)
            self.column(head, width=width[n], anchor=tk.W, stretch=tk.YES)

    def reset_data(self, data):
        self.remove_data()
        self.insert_data(data)

    def insert_data(self, data):
        for n in range(len(data)):
            current_info = [str(data[column][n]) for column in self.columns]
            self.insert('', tk.END, values=current_info)

    def remove_data(self):
        for row in self.get_children():
            self.delete(row)

    def set_style(self):
        style = ttk.Style(self)
        style.configure("Treeview", background="white",
                        fieldbackground="black", foreground="black")
        style.configure('Treeview.Heading', background="#76b9ff")
        style.configure('Treeview', rowheight=30)
        style.configure("Treeview", borderwidth=1, relief="solid")


class Graph_View:
    def __init__(self, df):
        self.df = df

    def histogram(self, root, attribute, min_range, max_range):
        fig = Figure(figsize=(10, 7), dpi=100, edgecolor='black', linewidth=2)
        canvas = FigureCanvasTkAgg(fig, master=root)

        plot = fig.add_subplot(1, 1, 1)
        plot.hist(self.df[attribute], bins=30, color='#76b9ff')

        plot.set_xlim(xmin=min_range, xmax=max_range)
        plot.set_xlabel(attribute)
        plot.set_ylabel('Number of Country')
        plot.set_title(f'{attribute} Histogram', fontsize=20, pad=20)

        canvas.draw()
        return canvas

    def scatter(self, root, x_attribute, min_x, max_x, y_attribute, min_y, max_y):
        fig = Figure(figsize=(10, 7), dpi=100, edgecolor='black', linewidth=2)
        canvas = FigureCanvasTkAgg(fig, master=root)

        plot = fig.add_subplot(1, 1, 1)
        plot.scatter(self.df[x_attribute], self.df[y_attribute], color='#76b9ff')

        plot.set_xlim(xmin=min_x, xmax=max_x)
        plot.set_ylim(ymin=min_y, ymax=max_y)
        plot.set_xlabel(x_attribute)
        plot.set_ylabel(y_attribute)
        plot.set_title(f'Scatter Plot between {x_attribute} and {y_attribute}', fontsize=16, pad=20)

        canvas.draw()
        return canvas

    def bar(self, root, data, x_attribute, y_attribute, min_y, max_y):
        fig = Figure(figsize=(10, 7), dpi=100, edgecolor='black', linewidth=2)
        canvas = FigureCanvasTkAgg(fig, master=root)

        plot = fig.add_subplot(1, 1, 1)
        plot.bar(data.index, data, color='#76b9ff')

        if len(data.index) <= 8:
            for i, v in enumerate(data):
                plot.text(i, v + 0.1, f'{int(v):,}', ha='center', va='bottom')

        if len(data.index) > 8:
            fig.subplots_adjust(bottom=0.2)
            plot.set_xticks(range(len(data.index)))
            plot.set_xticklabels(data.index, rotation=90, fontsize=6)

        plot.set_xlabel(x_attribute)
        plot.set_ylabel(y_attribute)
        plot.set_title(f'Bar Graph between {x_attribute} and {y_attribute}', fontsize=16, pad=20)

        canvas.draw()
        return canvas

    def box_plot(self, root, attribute):
        fig = Figure(figsize=(10, 7), dpi=100, edgecolor='black', linewidth=2)
        canvas = FigureCanvasTkAgg(fig, master=root)

        plot = fig.add_subplot(1, 1, 1)
        box = plot.boxplot(self.df[attribute], patch_artist=True)
        box['boxes'][0].set(facecolor='#76b9ff')

        plot.set_ylabel(attribute)
        plot.set_title(f'{attribute} Boxplot', fontsize=20, pad=20)

        canvas.draw()
        return canvas
