import omo
import time
import tkinter as tk
import tkinter.ttk as ttk
import appdirs
import csv
import os
import math

save_dir = appdirs.user_data_dir('Omo Trainer', 'PERVasive')
accident_log = os.path.join(save_dir, 'accidents.csv')


def now():
    return time.time()/60.0


class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Omo Trainer")
        try:
            img = tk.Image("photo", file="icon.png")
            self.root.call('wm', 'iconphoto', self.root._w, img)
        except tk.TclError:
            # If the icon is missing, just go on with the default icon
            pass

        self.drinker = omo.Drinker()

        self.load_data()

        # Initialize GUI property variables
        self.desperation = tk.DoubleVar()

        self.drink_amount = tk.IntVar()
        self.drink_amount.set(300)

        self.bladder_text = tk.StringVar()
        self.drink_text = tk.StringVar()
        self.permission_text = tk.StringVar()
        self.eta_text = tk.StringVar()

        self.create_widgets()
        self.create_menus()

        self.poll()

    def create_widgets(self):
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.bladder_bar = ttk.Progressbar(self.mainframe, orient=tk.VERTICAL,
                                           variable=self.desperation, maximum=1, mode='determinate')
        self.bladder_bar.grid(column=0, row=0, rowspan=2, sticky=(tk.N, tk.S))

        self.bladder_display = ttk.Label(self.mainframe, textvariable=self.bladder_text)
        self.bladder_display.grid(column=0, row=2, sticky=(tk.S, tk.W))

        self.eta_display = ttk.Label(self.mainframe, textvariable=self.eta_text)
        self.eta_display.grid(column=1, row=2, columnspan=2, sticky=(tk.S, tk.W))

        self.drink_slider = ttk.Scale(self.mainframe, orient=tk.HORIZONTAL, length=200,
                                      variable=self.drink_amount, command=self._quantize_drink, from_=100, to=750)
        self.drink_slider.grid(column=1, row=0, columnspan=2, sticky=(tk.W, tk.E))

        self.drink_display = ttk.Label(self.mainframe, textvariable=self.drink_text)
        self.drink_display.grid(column=3, row=0, sticky=(tk.E))
        self._quantize_drink()

        self.drink_button = ttk.Button(self.mainframe, text="Drink", command=self.drink)
        self.drink_button.grid(column=4, row=0, sticky=(tk.E))

        self.permission_text.set("May I pee?")
        self.permission_button = ttk.Button(self.mainframe, textvariable=self.permission_text,
                                            command=self.ask_permission)
        self.permission_button.grid(column=1, row=1, sticky=(tk.W))

        self.pee_button = ttk.Button(self.mainframe, text="Go pee.", command=self.pee)
        self.pee_button.grid(column=2, row=1, sticky=(tk.W))
        self.pee_button.state(['disabled'])

        self.accident_button = ttk.Button(self.mainframe, text="I can't hold it!", command=self.accident)
        self.accident_button.grid(column=4, row=1, sticky=(tk.E))

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def create_menus(self):
        self.menubar = tk.Menu(self.root, tearoff=0)
        self.menu_main = tk.Menu(self.menubar, tearoff=0)
        self.root.config(menu=self.menubar)
        self.menubar.add_cascade(menu=self.menu_main, label='Menu')
        self.menu_main.add_command(label='Reset Capacity Log', command=self.reset_capacity)

    def _quantize_drink(self, *args):
        value = self.drink_slider.get()
        quantized_val = int(round(value/50)*50)
        self.drink_amount.set(quantized_val)
        self.drink_text.set(str(quantized_val) + " mL")

    def _on_click(self, butt):
        """Briefly disables a button to avoid accidental double clicking"""
        butt.state(['disabled'])
        self.root.after(1000, lambda: butt.state(['!disabled']))

    def drink(self):
        self.drinker.add_drink(now(), self.drink_amount.get())
        self._on_click(self.drink_button)

    def accident(self):
        self.drinker.add_release(now(), False)
        self._on_click(self.accident_button)

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
        self.permission_text.set("May I pee?")
        self.pee_button.state(['disabled'])

    def poll(self):
        t = now()
        self.desperation.set(self.drinker.desperation(t))
        self.bladder_text.set(str(round(self.drinker.bladder(t))) + " mL/" + str(round(self.drinker.capacity)) + " mL")
        if self.drinker.eta:
            eta = math.ceil(self.drinker.eta - now())
            if eta > 1:
                self.eta_text.set("Potty emergency in: " + str(eta) + " minutes")
            elif eta == 1:
                self.eta_text.set("Potty emergency in: " + str(eta) + " minute")
            else:
                self.eta_text.set("Potty emergency now!")
        else:
            self.eta_text.set("")
        if self.permission_button.instate(['disabled']) and self.drinker.roll_allowed(t):
            self.permission_button.state(['!disabled'])
            self.pee_button.state(['disabled'])
            self.permission_text.set("May I pee?")
        self.root.after(500, self.poll)

    def load_data(self):
        if os.path.exists(accident_log):
            with open(accident_log, 'r', newline='') as f:
                reader = csv.reader(f)
                self.drinker.old_accidents = [float(row[0]) for row in reader]

    def save_data(self):
        os.makedirs(os.path.dirname(accident_log), exist_ok=True)
        with open(accident_log, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([accident.amount] for accident in self.drinker.accidents)

    def reset_capacity(self):
        if os.path.exists(accident_log):
            os.remove(accident_log)
        self.drinker.old_accidents = []


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
    app.save_data()

