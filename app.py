import omo
import tkinter as tk
import tkinter.ttk as ttk
import appdirs


class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Omo Trainer")

        self.create_widgets()

        self.poll()

    def create_widgets(self):
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.bladder_bar = ttk.Progressbar(self.mainframe, orient=tk.VERTICAL, mode='determinate')
        self.bladder_bar.grid(column=0, row=0, rowspan=2, sticky=(tk.N, tk.S))

        self.drink_slider = ttk.Scale(self.mainframe, orient=tk.HORIZONTAL, length=200, from_=50, to=750)
        self.drink_slider.grid(column=1, row=0, sticky=(tk.W, tk.E))

        self.drink_display = ttk.Label(self.mainframe)
        self.drink_display.grid(column=2, row=0, sticky=(tk.E))

        self.drink_button = ttk.Button(self.mainframe, text="Drink")
        self.drink_button.grid(column=3, row=0, sticky=(tk.E))

        self.permission_button = ttk.Button(self.mainframe, text="May I pee?")
        self.permission_button.grid(column=1, row=1, sticky=(tk.W))

        self.accident_button = ttk.Button(self.mainframe, text="I can't hold it!")
        self.accident_button.grid(column=3, row=1, sticky=(tk.E))

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def poll(self):
        self.root.after(500, self.poll)

app=App()
app.root.mainloop()

