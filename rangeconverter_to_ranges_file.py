# used for creating Postflop+ ranges

import fileinput


def count_commas(line_row):
    return line_row.count(',')


filename = "C:\\Users\\StefanPC\\Desktop\\Poker\\range_6.csv"

range_converter_range = input("Please paste range")
action = input("Please select hero action")
hero_position = input("Please select hero position")

if action != "OPEN":
    villain_position = input("Please select villain position")
else:
    villain_position = ""

hands = range_converter_range.split(",")

file = open(filename, "a+")

selected_hands = ""
for hand in hands:
    hand_and_frequency = hand.split(":")
    hand = hand_and_frequency[0]
    frequency_percentage = round(float(hand_and_frequency[1]) * 100)
    if frequency_percentage == 100:
        selected_hands += hand + ","
    else:
        selected_hands += "{}:{},".format(hand, frequency_percentage)
selected_hands = selected_hands[:-1]

file_row = "Range Converter,6,100,{},{},{},{}\n".format(action, hero_position,
                                                        villain_position, selected_hands)

file.write(file_row)
file.close()

print("Appended a line")
