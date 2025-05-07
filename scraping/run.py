"""
Script to run the data scraper for match and player data.
"""

import sys
import os

from match_data_select import match_data_select
from match_data_detailed_select import match_data_detailed_select
from player_data_select import player_data_select

def prompt_step(step_name):
    while True:
        resp = input(f"[PROMPT] Run step '{step_name}'? (y/n/exit): ").strip().lower()
        if resp in ("y", "n", "exit"): return resp
        print("Please enter 'y', 'n', or 'exit'.")

# Define the selection type for the dataset
# Options: 'NRL', 'NRLW', 'HOSTPLUS', 'KNOCKON'
SELECTION_TYPE = 'NRL'

# Define the year and round to fetch data for
SELECT_YEAR = 2025
SELECT_ROUND = 33

def main():
    print("\n==============================")
    print("[RUNNER] NRL Data Harvest Pipeline Start")
    print(f"[INFO] Year: {SELECT_YEAR}, Round: {SELECT_ROUND}, Comp: {SELECTION_TYPE}")
    print("==============================\n")

    # Step 1: Harvest Match Data
    resp = prompt_step("Harvest Match Data (basic results, teams, scores)")
    if resp == "y":
        match_data_select(SELECT_YEAR, SELECT_ROUND, SELECTION_TYPE)
    elif resp == "exit":
        sys.exit(0)

    # Step 2: Harvest Detailed Match Data
    resp = prompt_step("Harvest Detailed Match Data (in-depth stats, play-by-play)")
    if resp == "y":
        match_data_detailed_select(SELECT_YEAR, SELECT_ROUND, SELECTION_TYPE)
    elif resp == "exit":
        sys.exit(0)

    # Step 3: Harvest Player Stats (individual player statistics)
    resp = prompt_step("Harvest Player Stats (individual player statistics)")
    if resp == "y":
        player_data_select(SELECT_YEAR, SELECT_ROUND, SELECTION_TYPE)
    elif resp == "exit":
        sys.exit(0)

    print("\n[RUNNER] Data harvesting steps complete.\n")

if __name__ == "__main__":
    main()
