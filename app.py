import omo
import tkinter as tk
import tkinter.ttk as ttk
import appdirs

root = tk.Tk()
root.title("Omo Trainer")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

bladder_bar = ttk.Progressbar(mainframe, orient=tk.VERTICAL, length=200, mode='determinate')
bladder_bar.grid(column=1, sticky=(tk.N, tk.S))

drink_slider = ttk.Scale(mainframe, orient=tk.HORIZONTAL, length = 200, from_=50, to=750)
drink_slider.grid(column=2, row=1, sticky=(tk.W, tk.E))

drink_display = ttk.Label(mainframe)
drink_display.grid(column=3, row=1, sticky=(tk.E))

drink_button = ttk.Button(mainframe, text="Drink")
drink_button.grid(column=4, row=1, sticky=(tk.E))

permission_button = ttk.Button(mainframe, text="May I pee?")
permission_button.grid(column=2, row=2, sticky=(tk.W))

accident_button = ttk.Button(mainframe, text="I can't hold it!")
accident_button.grid(column=4, row=2, sticky=(tk.E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()

