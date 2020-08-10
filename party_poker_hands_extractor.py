import datetime
import os
import re
import sys
import time
from csv import reader
from pathlib import Path

import pytz
from dateutil import parser

edt_timezone = pytz.timezone('US/Eastern')
directory = sys.argv[1]
hand_history_filename = sys.argv[2]

original_hand_history_file = os.path.join(directory, hand_history_filename)

new_hand_history_filename = Path(original_hand_history_file).stem + "_selected.txt"

new_hand_history_file = os.path.join(directory, new_hand_history_filename)


def get_hours_between_london_and_edt():
    now = datetime.datetime.now()
    return (edt_timezone.localize(now) - pytz.timezone('Europe/London')
            .localize(now).astimezone(edt_timezone)).seconds / 3600


def poker_hand_matches(poker_hand, hand_needed):
    cards_arr = poker_hand.hero_cards
    return cards_arr[0] + cards_arr[1] == hand_needed or cards_arr[1] + cards_arr[0] == hand_needed


def difference_in_minutes(time1, time2):
    hour_difference = time1.hour - time2.hour
    minutes_difference = time1.minute - time2.minute
    return abs(hour_difference * 60 + minutes_difference)


file_hand_history = open(original_hand_history_file, 'r')


# TODO add this
def fix_whole_hand_bugs(whole_hand):
    return whole_hand


class PokerHand:
    def __init__(self, hero_cards, whole_hand, time):
        self.hero_cards = hero_cards
        self.whole_hand = whole_hand
        self.time = time

    def __repr__(self) -> str:
        return str(vars(self))


hand_history = file_hand_history.read()

hands = re.split(r'\n(?=\*{5}\sHand History)', hand_history)

poker_hands = []

for whole_hand in hands:
    hero_cards = re.search(r'Dealt to Hero\s\[(.*)\]', whole_hand).group(1).strip()
    hero_cards = list(map(lambda x: x.strip(), hero_cards.split(",")))
    time_regex_match = re.search(r'(?<=-\s).*\d{2} \d{2}:\d{2}:\d{2}.*\d{4}', whole_hand)
    time_as_string = time_regex_match.group()
    if "EDT" in time_as_string:
        time = parser.parse(time_as_string) + datetime.timedelta(
            hours=get_hours_between_london_and_edt())
    else:
        time = parser.parse(time_as_string)
    poker_hands.append(PokerHand(hero_cards, fix_whole_hand_bugs(whole_hand), time))

to_write_file = open(new_hand_history_file, "w")

with open(os.path.join(directory, 'hands_i_need_to_extract.csv'), 'r') as hands_need_extracting:
    csv_reader = reader(hands_need_extracting)
    for row in csv_reader:
        hand_needed = row[0]
        time_needed = time.strptime(row[1], "%H:%M")
        found_hands = list(filter(lambda x: poker_hand_matches(x, hand_needed), poker_hands))
        found_hands = sorted(found_hands, key=lambda x: difference_in_minutes(time_needed, x.time))
        if len(found_hands) > 0:
            to_write_file.write(found_hands[0].whole_hand)

to_write_file.close()
