import matplotlib.pyplot as plt
import numpy as np


def calculate_bluff_efficiency_needed(pot, bet):
    return round(100 / ((pot / bet) + 1))


def calculate_bluff_value_ratio_needed(pot, bet):
    pot_overall = pot + bet
    bluffs_needed = calculate_bluff_efficiency_needed(pot_overall, bet)
    return bluffs_needed, 100 - bluffs_needed


pot = 200
bet = 25

# plotting bluff efficiency needed for pot
x = np.linspace(1, 4 * pot, 20)
y = np.array([calculate_bluff_efficiency_needed(pot, b) for b in x])

figure = plt.figure()

axes = figure.add_axes([0.1, 0.1, 0.8, 0.8])

axes.plot(x, y, 'b')
axes.set_xlabel('Size of Bet')
axes.set_ylabel('% That The Bluff Needs To Work')
axes.set_title('Bluff Efficiency Needed for {} pot'.format(pot))

figure.show()

# plotting bluffs vs value ratio in pie chart format
labels_with_colors = {'Bluff': 'r', 'Value': 'g'}
bluff_value_ratio = calculate_bluff_value_ratio_needed(pot, bet)

fig1, ax1 = plt.subplots()

ax1.pie(bluff_value_ratio, labels=labels_with_colors.keys(),
        colors=labels_with_colors.values(),
        autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.title('Bluff to Value Ratio for betting {} into {}'.format(bet, pot))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

fig1.show()
