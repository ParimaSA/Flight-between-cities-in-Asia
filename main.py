"""Module for Quality of Life App"""
from app import App_Controller
from model import Model
from view import View


if __name__ == '__main__':
    model = Model()
    view = View()
    app = App_Controller(model=model, view=view)
    app.run()
