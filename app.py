"""Module for App Controller class."""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from graph_state import Histogram, Scatter_Plot, Bar_Graph, Box_Plot


class App_Controller(tk.Tk):
    """Main UI for Quality of Life App"""

    def __init__(self, model, view):
        """Initialize the App"""
        super().__init__()
        self.title('Quality of Life')
        self.model = model
        self.view = view
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.current_frame = None
        self.set_frame(Home_Page)

    def set_frame(self, frame):
        """Change page to the select frame"""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame(self, self.frame)
        self.current_frame.pack(expand=True, fill=tk.BOTH)

    def run(self):
        """Run the App"""
        self.mainloop()

    def exit(self):
        """Exit the App"""
        self.destroy()


class DemoPage(tk.Frame):
    """The demo for every page"""
    head_button = {'font': ('Ariel', 25, 'bold'), 'fg': '#a6a6a6', 'bg': '#f8f5ef', 'bd': 1, 'relief': tk.FLAT}
    head_pack = {'side': tk.RIGHT, 'padx': 15, 'pady': 10}

    def __init__(self, main_window, frame):
        """Initialize the page"""
        super().__init__(frame)
        self.main = main_window
        self.head_frame = tk.Frame(self, bg='#f8f5ef')

    def init_head_components(self):
        """Initialize the head button to navigate between each page"""
        home_button = self.create_button(self.head_frame, 'HOME', self.home_button_handler, self.head_button)
        home_button.pack(side=tk.LEFT, padx=15, pady=20)

    def init_components(self):
        """Initialize the components in the page"""
        pass

    def create_button(self, root, text: str, bind, opt):
        """Create and Return the button with the option from the parameters"""
        button = tk.Button(root, text=text, **opt)
        button.bind('<Button>', bind)
        return button

    def home_button_handler(self, *args):
        """Set the page to Home page"""
        self.main.set_frame(Home_Page)

    def button_handler(self, event, *args):
        """Set page from button"""
        frame_dict = {'Quality of Life Data': Data_Table_Page, 'Data Storytelling': Storytelling_Page,
                      'Create Graph': Graph_Page, 'Storytelling': Storytelling_Page}
        key = event.widget['text']
        self.main.set_frame(frame_dict[key])


class Home_Page(DemoPage):
    """Main Page with the button to the other page"""
    button_opt = {'font': ('Ariel', 40, 'bold'), 'height': 1, 'bg': '#fac0d6'}

    def __init__(self, main_window, frame):
        """Initialize the Home page"""
        super().__init__(main_window, frame)
        self.img = Image.open('background//home.png')
        self.init_components()

    def init_head_components(self):
        """Initialize head components in home page, navigate to home or close the app"""
        super().init_head_components()
        exit_button = self.create_button(self.head_frame, 'EXIT', self.exit_button_handler, self.head_button)
        exit_button.pack(**self.head_pack)

    def init_components(self):
        """Initialize the components in Home page"""
        self.init_head_components()
        self.head_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)

        bg_frame = self.create_background_frame()
        self.button_frame = self.create_button_frame()

        bg_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.button_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def create_background_frame(self):
        """Create the Frame contain the logo image of the App"""
        frame = tk.Frame(self, bg='#f8f5ef')
        self.bg = ImageTk.PhotoImage(self.img)
        self.image_label = tk.Label(frame, image=self.bg, borderwidth=0)
        self.image_label.pack(expand=True)
        self.bind('<Configure>', self.resize)  # change the size of the image when resize the window
        return frame

    def resize(self, *args):
        """Resizing the logo image and button text size"""
        self.update()
        new_width = int(self.head_frame.winfo_width() * 2/3)
        new_height = int(new_width/1920 * 1080)
        if new_height == 0 or new_width == 0:
            return

        resized_img = self.img.resize((new_width, new_height))
        self.bg = ImageTk.PhotoImage(resized_img)
        self.image_label.configure(image=self.bg)

        font_size = self.main.winfo_width()//40 - 2

        self.button_opt['font'] = ('Ariel', font_size, 'bold')
        self.button_frame.pack_forget()
        self.button_frame = self.create_button_frame()
        self.button_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def create_button_frame(self):
        """Create and Return the frame with button to other pages"""
        big_frame = tk.Frame(self, bg='#f8f5ef')
        frame = tk.Frame(big_frame, bg='#f8f5ef')
        data_button = self.create_button(frame, 'Quality of Life Data', self.button_handler, self.button_opt)
        story_button = self.create_button(frame, 'Data Storytelling', self.button_handler, self.button_opt)
        graph_button = self.create_button(frame, 'Create Graph', self.button_handler, self.button_opt)

        pack_opt = {'side': tk.TOP, 'fill': tk.X, 'padx': 30, 'pady': 30}
        data_button.pack(**pack_opt)
        story_button.pack(**pack_opt)
        graph_button.pack(**pack_opt)
        frame.pack(expand=True)

        return big_frame

    def exit_button_handler(self, *args):
        """Close the App"""
        self.main.exit()


class Data_Table_Page(DemoPage):
    """Page showing the quality of life data in table form"""

    def __init__(self, main_window, frame):
        """Initialize the Data Table page"""
        super().__init__(main_window, frame)
        self.img = Image.open('background//qol_title.png')
        self.sort = tk.StringVar()  # variable for sorting the data
        self.switch_var = ctk.StringVar(value="off")  # data form switch variable
        self.init_components()

    def init_head_components(self):
        """Initialize head components in Data page, navigate to Storytelling and Graph page"""
        super().init_head_components()
        story_button = self.create_button(self.head_frame, 'Storytelling', self.button_handler, self.head_button)
        graph_button = self.create_button(self.head_frame, 'Create Graph', self.button_handler, self.head_button)
        story_button.pack(**self.head_pack)
        graph_button.pack(**self.head_pack)

    def init_components(self):
        """Initialize components in Data Table page"""
        self.init_head_components()
        self.head_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)

        title_frame = self.create_title_frame()
        title_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, anchor=tk.N)

        tree_frame = self.init_treeview()
        self.tree.reset_data(self.main.model.data)
        tree_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def create_title_frame(self):
        """Create and Return the title frame contain title, part for select sorting attribute, switch the data form"""
        frame = tk.Frame(self, height=120, bg='#f8f5ef')
        resized_img = self.img.resize((int(120/500*1920), 120))
        self.bg = ImageTk.PhotoImage(resized_img)
        self.image_label = tk.Label(frame, image=self.bg, borderwidth=0)
        self.image_label.pack(side=tk.LEFT, anchor=tk.NW, padx=40)

        sort_frame = self.create_sort_frame(frame)
        sort_frame.pack(side=tk.LEFT, pady=20, fill=tk.BOTH, expand=True, anchor=tk.NW)

        table = tk.Label(frame, text='table', borderwidth=0, font=("Ariel", 12), bg='#f8f5ef')
        form_switch = ctk.CTkSwitch(frame, text="country", command=self.switch_handler, variable=self.switch_var,
                                    onvalue="on", offvalue="off", switch_width=100, switch_height=25,
                                    fg_color="#76b9ff", progress_color="#76b9ff", font=("Ariel", 16),)
        form_switch.pack(side=tk.RIGHT, pady=10, padx=20)
        table.pack(side=tk.RIGHT, pady=10)

        return frame

    def switch_handler(self, *args):
        """Change to Data Country Page"""
        self.main.set_frame(Data_Country_Page)

    def create_sort_frame(self, title_frame):
        """Create and Return the sort frame, contain the label and combobox for sorting attribute"""
        frame = tk.Frame(title_frame, bg='#f8f5ef')
        font_option = {'font': ('Ariel', 16)}

        sort_label = tk.Label(frame, text='Sort by', **font_option, bg='#f8f5ef')

        sort_by = ttk.Combobox(frame, width=27, textvariable=self.sort, **font_option, state='readonly')
        sort_by['values'] = self.main.model.index_columns()
        sort_by.current(newindex=0)
        sort_by.bind("<<ComboboxSelected>>", self.sort_tree)

        self.info_label = tk.Label(frame, text='(Higher is Better)', **font_option, fg='DodgerBlue4', bg='#f8f5ef')

        pack_opt = {'side': tk.LEFT, 'expand': False, 'fill': tk.X, 'pady': 5, 'padx': 10}
        sort_label.pack(**pack_opt)
        sort_by.pack(**pack_opt)
        self.info_label.pack(**pack_opt)

        return frame

    def init_treeview(self):
        """Initialize treeview for containing the data"""
        frame = tk.Frame(self, bg='#f8f5ef')
        columns = list(self.main.model.columns())
        columns.remove('Continent')
        columns.remove('Population')
        columns.remove('Area')
        columns.remove('Density')
        self.tree = self.main.view.data(frame, columns)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=80, pady=40)
        return frame

    def sort_tree(self, event, *args):
        """Sort the data with sorting attribute and put it in the treeview"""
        event.widget.selection_clear()
        sort_by = self.sort.get()
        sort_data = self.main.model.sort_data(sort_by)
        self.tree.reset_data(sort_data)

        info = '(Higher is Better)'
        if sort_by in self.main.model.lower_value():
            info = '(Lower is Better)'
        self.info_label.config(text=info)


class Data_Country_Page(DemoPage):
    """Page showing the quality of life data in country form"""

    def __init__(self, main_window, frame):
        super().__init__(main_window, frame)
        self.img = Image.open('background//qol_title.png')
        self.country = tk.StringVar()  # country attribute to filter the data
        self.switch_var = ctk.StringVar(value="on")  # data form switch variable
        self.init_components()

    def init_head_components(self):
        """Initialize head components in Data page, navigate to Storytelling and Graph page"""
        super().init_head_components()
        story_button = self.create_button(self.head_frame, 'Storytelling', self.button_handler, self.head_button)
        graph_button = self.create_button(self.head_frame, 'Create Graph', self.button_handler, self.head_button)
        story_button.pack(**self.head_pack)
        graph_button.pack(**self.head_pack)

    def init_components(self):
        """Initialize components in Data Country page"""
        self.init_head_components()
        self.head_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)

        title_frame = self.create_title_frame()
        title_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)
        self.data_frame = self.create_data_frame()
        self.data_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def create_title_frame(self):
        """Create and Return the title frame contain title, part for country attribute, switch data form"""
        frame = tk.Frame(self, height=120, bg='#f8f5ef')
        resized_img = self.img.resize((int(120/500*1920), 120))
        self.bg = ImageTk.PhotoImage(resized_img)
        self.image_label = tk.Label(frame, image=self.bg, borderwidth=0)
        self.image_label.pack(side=tk.LEFT, anchor=tk.NW, padx=40)

        country_frame = self.create_country_select(frame)
        country_frame.pack(side=tk.LEFT, pady=20, fill=tk.BOTH, expand=True, anchor=tk.NW)

        table = tk.Label(frame, text='table', borderwidth=0, font=("Ariel", 12), bg='#f8f5ef')
        form_switch = ctk.CTkSwitch(frame, text="country", command=self.switch_handler, variable=self.switch_var,
                                    onvalue="on", offvalue="off", switch_width=100, switch_height=25,
                                    fg_color="#338be6", progress_color="#338be6", font=("Ariel", 16),)
        form_switch.pack(side=tk.RIGHT, pady=10, padx=20)
        table.pack(side=tk.RIGHT, pady=10)
        return frame

    def switch_handler(self, *args):
        """Change to Data Table page"""
        self.main.set_frame(Data_Table_Page)

    def create_data_frame(self, *args):
        """Create and return frame, contain info and index of the country"""
        self.select_country.selection_clear()
        country = self.country.get()
        country_data = self.main.model.filter_data({'Country': country})
        country_data_frame = tk.Frame(self, bg='#f8f5ef')

        self.create_country_info(country_data_frame, country, country_data)

        columns = self.main.model.index_columns()[1:]
        colors = ['#ff5b6e', '#f46d43', '#fdae61', '#c6e792', '#e6f598', '#ffffbf', '#abdda4', '#66c2a5', '#3288bd']
        self.create_all_index_frame(country_data_frame, country_data, columns, colors)
        country_data_frame.columnconfigure(0, weight=1)
        country_data_frame.columnconfigure(1, weight=1)
        country_data_frame.rowconfigure(0, weight=1)
        return country_data_frame

    def create_country_info(self, country_frame, country, country_data):
        """Create frame contain info of the country in data frame"""
        frame = tk.Frame(country_frame, bg='#f8f5ef', borderwidth=2, relief='solid')
        title_frame = self.create_country_name_frame(frame, country, list(country_data["Continent"])[0])
        title_frame.pack(side=tk.TOP, pady=20, padx=20, expand=True, fill=tk.BOTH)

        middle_frame = tk.Frame(frame, bg='#f8f5ef')
        middle_opt = {'font': ('Ariel', 20), 'anchor': tk.W, 'bg': '#f8f5ef'}
        middle_pack = {'side': tk.TOP, 'padx': 5, 'pady': 10, 'anchor': tk.NW, 'fill': tk.X}
        area = tk.Label(middle_frame, text=f'Area: {list(country_data["Area"])[0]:,} kilometer per square',
                        **middle_opt)
        pop = tk.Label(middle_frame, text=f'Population: {list(country_data["Population"])[0]:,}', **middle_opt)
        dens = tk.Label(middle_frame, text=f'Population Density: {list(country_data["Density"])[0]} per square '
                                           f'kilometer', **middle_opt)
        area.pack(**middle_pack)
        pop.pack(**middle_pack)
        dens.pack(**middle_pack)

        middle_frame.pack(side=tk.TOP, pady=20, padx=20,  expand=True, fill=tk.BOTH)

        last_frame = self.create_rank_frame(frame, country_data)
        last_frame.pack(side=tk.TOP, fill=tk.X)

        frame.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)

    def create_country_select(self, title_frame):
        """Create and return the frame contain part for select the country"""
        font_option = {'font': ('Ariel', 16)}
        frame = tk.Frame(title_frame, bg='#f8f5ef')
        country_label = tk.Label(frame, text='Country', **font_option, bg='#f8f5ef')

        self.select_country = ttk.Combobox(frame, textvariable=self.country, state='readonly', **font_option)
        self.select_country['values'] = self.main.model.country_name()
        self.select_country.current(newindex=0)
        self.select_country.bind('<<ComboboxSelected>>', self.set_data)

        pack_opt = {'side': tk.LEFT, 'expand': False, 'fill': tk.X, 'pady': 5, 'padx': 10}
        country_label.pack(**pack_opt)
        self.select_country.pack(**pack_opt)
        return frame

    def create_rank_frame(self, country_frame, data):
        """Create and return frame contain quality of life index and rank of the country"""
        frame = tk.Frame(country_frame, height=30, bg='#f8f5ef')
        qol = tk.Label(frame, text=f'Quality of Life Index {list(data["Quality of Life Index"])[0]}',
                       font=('Ariel', 30), borderwidth=1, relief='solid', bg='#fac0d6')
        rank = tk.Label(frame, text=f'Rank {list(data["Rank"])[0]}', font=('Ariel', 40), borderwidth=1, relief='solid',
                        bg='#fac0d6')

        rank.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        qol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        return frame

    def create_all_index_frame(self, country_frame, data, column, color):
        """Create frame contain all index in data frame"""
        frame = tk.Frame(country_frame, bg='#f8f5ef')
        for h in range(9):
            label = self.index_frame(frame, column[h], list(data[column[h]])[0], color[h])
            label.grid(row=h//3, column=h % 3, sticky=tk.NSEW, padx=3, pady=3)

        for i in range(3):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i, weight=1)

        frame.grid(row=0, column=1, sticky=tk.NSEW, padx=20, pady=50)

    def index_frame(self, all_frame, head, info, color):
        """Create and return index frame contain head and value for each index"""
        size = 17
        if len(head) > 20:
            size = 12
        frame = tk.Frame(all_frame, bg=color, borderwidth=2, relief='solid')
        label_head = tk.Label(frame, text=head, font=('Ariel', size), bg=color)
        label_info = tk.Label(frame, text=info, font=('Ariel', 35), bg=color)
        label_head.pack(side=tk.TOP, expand=True)
        label_info.pack(side=tk.TOP, expand=True)
        return frame

    def create_country_name_frame(self, data_frame, country, continent):
        """Create and return the frame contain name and continent of the country"""
        frame = tk.Frame(data_frame, bg='#f8f5ef')
        country = tk.Label(frame, text=country, font=('Ariel', 40), bg='#f8f5ef')
        continent = tk.Label(frame, text=f'({continent})', font=('Ariel', 20), bg='#f8f5ef')
        country.pack(side=tk.LEFT)
        continent.pack(side=tk.LEFT, padx=40)
        return frame

    def set_data(self, event, *args):
        """Change all data to the selected country"""
        event.widget.selection_clear()
        self.data_frame.destroy()
        self.data_frame = self.create_data_frame()
        self.data_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)


class Storytelling_Page(DemoPage):
    """Page showing the storytelling"""

    def __init__(self, main_window, frame):
        """Initialize the Storytelling page"""
        super().__init__(main_window, frame)
        self.img = Image.open('background//storytelling.png')  # Replace with your image file path
        self.init_components()

    def init_head_components(self):
        """Initialize head components for Storytelling page, navigation button to data and graph page"""
        super().init_head_components()
        qol_button = self.create_button(self.head_frame, 'Quality of Life Data', self.button_handler, self.head_button)
        graph_button = self.create_button(self.head_frame, 'Create Graph', self.button_handler, self.head_button)
        graph_button.pack(**self.head_pack)
        qol_button.pack(**self.head_pack)

    def init_components(self):
        """Initialize components in Storytelling page"""
        self.init_head_components()
        self.head_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)

        bg_frame = self.create_background_frame()
        bg_frame.pack(expand=True, fill=tk.BOTH)

    def create_background_frame(self):
        """Create and Return the frame with image label"""
        frame = tk.Frame(self, bg='#f8f5ef')
        self.bg = ImageTk.PhotoImage(self.img)
        self.image_label = tk.Label(frame, image=self.bg, borderwidth=0)
        self.image_label.pack(expand=True)
        self.bind('<Configure>', self.resize)  # resize image when resize the App
        return frame

    def resize(self, *args):
        """Function resizing the image size"""
        self.update()
        new_height = self.main.winfo_height() - 80
        new_width = int(new_height/1080 * 1920)
        if new_height == 0 or new_width == 0:
            return

        resized_img = self.img.resize((new_width, new_height))
        self.bg = ImageTk.PhotoImage(resized_img)
        self.image_label.configure(image=self.bg)


class Graph_Page(DemoPage):
    """Page for create graph from the user input"""
    graph_class = {'Histogram': Histogram, 'Scatter': Scatter_Plot, 'Bar Graph': Bar_Graph, 'Box Plot': Box_Plot}

    def __init__(self, window_frame, frame):
        """Initialize the Graph page"""
        super().__init__(window_frame, frame)
        self.img = Image.open('background//graph_title.png')
        self.graph = tk.StringVar()
        self.state = Histogram
        self.init_components()

    def init_head_components(self):
        """Initialize head components, navigate to data and storytelling page"""
        super().init_head_components()
        qol_button = self.create_button(self.head_frame, 'Quality of Life Data', self.button_handler, self.head_button)
        story_button = self.create_button(self.head_frame, 'Storytelling', self.button_handler, self.head_button)
        qol_button.pack(**self.head_pack)
        story_button.pack(**self.head_pack)

    def init_components(self):
        """Initialize components in Graph page"""
        self.init_head_components()
        self.head_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)

        title_frame = self.create_title_frame()
        title_frame.pack(side=tk.TOP, expand=False, fill=tk.X, anchor=tk.N)

        self.graph_frame = tk.Frame(self, bg='#f8f5ef')
        self.create_graph_view(self.graph_frame)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.current_graph = self.state(self.graph_frame, self.main.model, self.graph_view)

    def create_graph_view(self, graph_frame):
        """Create Graph View in graph frame"""
        frame = tk.Frame(graph_frame, bg='white')
        self.graph_view = self.main.view.graph(frame)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=40, pady=30)

    def create_title_frame(self):
        """Create and Return title frame, contain the title and part for select the graph type"""
        frame = tk.Frame(self, height=120, bg='#f8f5ef')
        resized_img = self.img.resize((int(120 / 500 * 1920), 120))
        self.bg = ImageTk.PhotoImage(resized_img)
        self.image_label = tk.Label(frame, image=self.bg, borderwidth=0)
        self.image_label.pack(side=tk.LEFT, anchor=tk.NW, padx=40)

        type_frame = self.create_type_frame(frame)
        type_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        return frame

    def create_type_frame(self, title_frame):
        """Create and Return type frame in title frame with label and combobox for graph type attribute"""
        frame = tk.Frame(title_frame, bg='#f8f5ef')
        font_option = {'font': ('Ariel', 16)}

        type_label = tk.Label(frame, text='Type', **font_option, bg='#f8f5ef')

        select_graph = ttk.Combobox(frame, width=27, textvariable=self.graph, state='readonly', **font_option)
        select_graph['values'] = ['Histogram', 'Scatter', 'Bar Graph', 'Box Plot']
        select_graph.current(newindex=0)
        select_graph.bind('<<ComboboxSelected>>', self.change_type)

        pack_opt = {'side': tk.LEFT, 'expand': False, 'fill': tk.X, 'pady': 5, 'padx': 10}
        type_label.pack(**pack_opt)
        select_graph.pack(**pack_opt)

        return frame

    def change_type(self, event, *args):
        """Change the graph state to the selected type"""
        event.widget.selection_clear()
        self.current_graph.attribute_frame.destroy()
        self.state = self.graph_class[self.graph.get()]
        self.current_graph = self.state(self.graph_frame, self.main.model, self.graph_view)
