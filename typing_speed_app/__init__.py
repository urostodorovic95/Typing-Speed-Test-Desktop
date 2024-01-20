from . import gui


def main_app():
    app = gui.AppWindow()
    gui.MainFrame(parent=app)
    app.mainloop()
