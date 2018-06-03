import omo
import time
import tkinter as tk
import tkinter.ttk as ttk
import appdirs

def now():
    return time.time()/60.0

class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Omo Trainer")

        self.drinker = omo.Drinker()

        self.load_data()

        # Initialize GUI property variables
        self.desperation = tk.DoubleVar()

        self.drink_amount = tk.IntVar()
        self.drink_amount.set(300)

        self.create_widgets()

        self.poll()

    def create_widgets(self):
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.bladder_bar = ttk.Progressbar(self.mainframe, orient=tk.VERTICAL,
                                           variable=self.desperation, maximum=1, mode='determinate')
        self.bladder_bar.grid(column=0, row=0, sticky=(tk.N, tk.S))

        # self.bladder_display = ttk.Label(self.mainframe, textvariable=self.desperation)
        # self.bladder_display.grid(column=0, row=0, sticky=(tk.N, tk.E))

        self.drink_slider = ttk.Scale(self.mainframe, orient=tk.HORIZONTAL, length=200,
                                      variable=self.drink_amount, command=self.quantize_drink, from_=50, to=750)
        self.drink_slider.grid(column=1, row=0, columnspan=2, sticky=(tk.W, tk.E))

        self.drink_display = ttk.Label(self.mainframe, textvariable=self.drink_amount)
        self.drink_display.grid(column=3, row=0, sticky=(tk.E))

        self.drink_units = ttk.Label(self.mainframe, text="mL")
        self.drink_units.grid(column=4, row=0, sticky=(tk.W))

        self.drink_button = ttk.Button(self.mainframe, text="Drink", command=self.drink)
        self.drink_button.grid(column=5, row=0, sticky=(tk.E))

        self.permission_text = tk.StringVar()
        self.permission_text.set("May I pee?")
        self.permission_button = ttk.Button(self.mainframe, textvariable=self.permission_text,
                                            command=self.ask_permission)
        self.permission_button.grid(column=1, row=1, sticky=(tk.W))

        self.pee_button = ttk.Button(self.mainframe, text="Go pee.", command=self.pee)
        self.pee_button.grid(column=2, row=1, sticky=(tk.W))
        self.pee_button.state(['disabled'])

        self.accident_button = ttk.Button(self.mainframe, text="I can't hold it!", command=self.accident)
        self.accident_button.grid(column=5, row=1, sticky=(tk.E))

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def quantize_drink(self, *args):
        value = self.drink_slider.get()
        quantized_val = int(round(value/50)*50)
        self.drink_amount.set(quantized_val)

    def drink(self):
        self.drinker.add_drink(now(), self.drink_amount.get())

    def accident(self):
        self.drinker.add_release(now(), False)

    def ask_permission(self):
        if self.drinker.roll_for_permission(now()):
            self.permission_text.set("You may pee.")
            self.permission_button.state(['disabled'])
            self.pee_button.state(['!disabled'])
        else:
            self.permission_text.set("You may not pee.")
            self.permission_button.state(['disabled'])

    def pee(self):
        self.drinker.add_release(now(), True)
        self.pee_button.state(['disabled'])

    def poll(self):
        t = now()
        self.desperation.set(self.drinker.desperation(t))
        if self.permission_button.instate(['disabled']) and self.drinker.roll_allowed(t):
            self.permission_button.state(['!disabled'])
            self.pee_button.state(['disabled'])
            self.permission_text.set("May I pee?")
        self.root.after(500, self.poll)

    def load_data(self):
        pass


app = App()
app.root.mainloop()

