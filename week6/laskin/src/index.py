from tkinter import Tk
from ui import UI
from application_logic import ApplicationLogic


def main():
    application = ApplicationLogic()

    window = Tk()
    window.title("Calculator")

    ui = UI(application, window)
    ui.start()

    window.mainloop()

if __name__ == "__main__":
    main()
