import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox


def calculate_bluff_efficiency_needed(pot, bet):
    return round(100 / ((pot / bet) + 1))


def calculate_bluff_value_ratio_needed(pot, bet):
    pot_overall = pot + bet
    bluffs_needed = calculate_bluff_efficiency_needed(pot_overall, bet)
    return bluffs_needed, 100 - bluffs_needed


# gui
root = tk.Tk()

tk.Label(root, text="Pot Size: ").grid(row=0, column=0, padx=10, pady=10)
pot_size = tk.IntVar()
tk.Entry(root, textvariable=pot_size).grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Bet Size: ").grid(row=1, column=0, padx=10, pady=10)
bet_size = tk.IntVar()
tk.Entry(root, textvariable=bet_size).grid(row=1, column=1, padx=10, pady=10)

plots_frame = tk.Frame(root)
plots_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)


def validate_and_get(tk_var):
    try:
        val = tk_var.get()
        if val <= 0:
            messagebox.showerror("Error", "Both Bet and Pot "
                                          "should be bigger than 0")
            return None
        return val
    except tk.TclError:
        messagebox.showerror("Error", "Both Bet and Pot should be provided")
        return None


# display plots
def display_charts():
    pot = validate_and_get(pot_size)
    if pot is None:
        return
    bet = validate_and_get(bet_size)
    if bet is None:
        return

    # clear frame
    for widget in plots_frame.winfo_children():
        widget.destroy()
    # plotting bluff efficiency needed for pot
    x = np.linspace(1, max(4 * pot, bet), 20)
    y = np.array([calculate_bluff_efficiency_needed(pot, b) for b in x])

    figure = plt.figure()

    axes = figure.add_axes([0.1, 0.1, 0.8, 0.8])

    axes.plot(x, y, 'b')
    axes.set_xlabel('Size of Bet')
    axes.set_ylabel('% That The Bluff Needs To Work')
    axes.set_title('Bluff Efficiency Needed for {} pot'.format(pot))

    FigureCanvasTkAgg(figure, plots_frame).get_tk_widget().pack(side="left")

    # plotting bluffs vs value ratio in pie chart format
    labels_with_colors = {'Bluff': 'r', 'Value': 'g'}
    bluff_value_ratio = calculate_bluff_value_ratio_needed(pot, bet)

    fig1, ax1 = plt.subplots()

    ax1.pie(bluff_value_ratio, labels=labels_with_colors.keys(),
            colors=labels_with_colors.values(),
            autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Bluff to Value Ratio for betting {} into {} \n to'
              ' make opponent indifferent to calling/folding'.format(bet, pot))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    FigureCanvasTkAgg(fig1, plots_frame).get_tk_widget().pack(side="left")


tk.Button(root, text="Display Charts", command=display_charts).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.title('Bluff Efficiency Plotting')
root.mainloop()
