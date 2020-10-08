import pyperclip
import sys

rangeconverter_range = sys.argv[1]

hands = rangeconverter_range.split(",")

solver_friendly_range = ""

for hand in hands:
    hand_and_frequency = hand.split(":")
    hand = hand_and_frequency[0]
    frequency_percentage = round(float(hand_and_frequency[1]) * 100)
    solver_friendly_range += "[" + str(frequency_percentage) + "]" + hand + "[/" + str(frequency_percentage) + "],"

solver_friendly_range = solver_friendly_range[:-1]

pyperclip.copy(solver_friendly_range)

print("Solver Range copied to clipboard")

