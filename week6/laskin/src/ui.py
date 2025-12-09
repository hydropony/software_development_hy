from enum import Enum
from tkinter import ttk, constants, StringVar


class Command(Enum):
    SUM = 1
    DIFFERENCE = 2
    RESET = 3
    UNDO = 4


class Sum:
    def __init__(self, application_logic, read_input):
        self._application_logic = application_logic
        self._read_input = read_input

    def execute(self):
        try:
            value = int(self._read_input())
        except Exception:
            value = 0
        self._application_logic.add(value)


class Difference:
    def __init__(self, application_logic, read_input):
        self._application_logic = application_logic
        self._read_input = read_input

    def execute(self):
        try:
            value = int(self._read_input())
        except Exception:
            value = 0
        self._application_logic.subtract(value)


class Reset:
    def __init__(self, application_logic, read_input):
        self._application_logic = application_logic
        self._read_input = read_input

    def execute(self):
        self._application_logic.reset()


class Undo:
    def __init__(self, application_logic, read_input):
        self._application_logic = application_logic
        self._read_input = read_input

    def execute(self):
        self._application_logic.undo()


class UI:
    def __init__(self, application_logic, root):
        self._application_logic = application_logic
        self._root = root

        # store commands in a dictionary
        self._commands = {
            Command.SUM: Sum(application_logic, self._read_input),
            Command.DIFFERENCE: Difference(application_logic, self._read_input),
            Command.RESET: Reset(application_logic, self._read_input),
            Command.UNDO: Undo(application_logic, self._read_input)
        }

    def _read_input(self):
        return self._input_field.get()

    def start(self):
        self._value_var = StringVar()
        self._value_var.set(self._application_logic.value())
        self._input_field = ttk.Entry(master=self._root)

        result_label = ttk.Label(textvariable=self._value_var)

        sum_button = ttk.Button(
            master=self._root,
            text="Sum",
            command=lambda: self._execute_command(Command.SUM)
        )

        difference_button = ttk.Button(
            master=self._root,
            text="Difference",
            command=lambda: self._execute_command(Command.DIFFERENCE)
        )

        self._reset_button = ttk.Button(
            master=self._root,
            text="Reset",
            state=constants.DISABLED,
            command=lambda: self._execute_command(Command.RESET)
        )

        self._undo_button = ttk.Button(
            master=self._root,
            text="Undo",
            state=constants.DISABLED,
            command=lambda: self._execute_command(Command.UNDO)
        )

        result_label.grid(columnspan=4)
        self._input_field.grid(columnspan=4, sticky=(constants.E, constants.W))
        sum_button.grid(row=2, column=0)
        difference_button.grid(row=2, column=1)
        self._reset_button.grid(row=2, column=2)
        self._undo_button.grid(row=2, column=3)

    def _execute_command(self, command):
        # get the correct command from the dictionary
        command_object = self._commands[command]
        command_object.execute()

        self._undo_button["state"] = constants.NORMAL

        if self._application_logic.value() == 0:
            self._reset_button["state"] = constants.DISABLED
        else:
            self._reset_button["state"] = constants.NORMAL

        self._input_field.delete(0, constants.END)
        self._value_var.set(self._application_logic.value())
