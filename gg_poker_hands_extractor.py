import glob
import os
import re
import sys

directory = sys.argv[1]
hand_history_directory = sys.argv[2]

hand_id_to_extract = input("Please enter id of the hand:")

if not hand_id_to_extract.strip():
    sys.exit()

hand_history_extract = os.path.join(directory, hand_history_directory + "_hh.txt")

to_write_file = open(hand_history_extract, "a")

for hand_history_file in glob.glob(os.path.join(directory, hand_history_directory + "\**.txt")):
    with open(hand_history_file, 'r') as file:
        hands = re.split(r'\n(?=Poker Hand)', file.read())
        for hand in hands:
            if hand_id_to_extract in hand:
                to_write_file.write(hand)

to_write_file.close()
