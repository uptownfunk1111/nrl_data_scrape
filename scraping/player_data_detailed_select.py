"""
Scrape and aggregate detailed NRL player statistics for each match in a given year and round range.
Outputs a JSON file in the same format as player_data_select.py, but with additional advanced stats per player.
"""
import os
import sys
import json
# Ensure ENVIRONMENT_VARIABLES is imported from the correct location
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import ENVIRONMENT_VARIABLES as EV
from utilities.set_up_driver import set_up_driver
from bs4 import BeautifulSoup

def player_data_detailed_select(SELECT_YEAR, SELECT_ROUND, SELECTION_TYPE):
    selection_mapping = {
        'NRLW': (EV.NRLW_TEAMS, EV.NRLW_WEBSITE),
        'KNOCKON': (EV.KNOCKON_TEAMS, EV.KNOCKON_WEBSITE),
        'HOSTPLUS': (EV.HOSTPLUS_TEAMS, EV.HOSTPLUS_WEBSITE)
    }
    WEBSITE = EV.NRL_WEBSITE
    TEAMS = EV.TEAMS
    TEAMS, WEBSITE = selection_mapping.get(SELECTION_TYPE, (TEAMS, WEBSITE))
    player_stats_file = f"../data/{SELECTION_TYPE}/{SELECT_YEAR}/{SELECTION_TYPE}_player_detailed_statistics_{SELECT_YEAR}.json"
    match_data_file = f"../data/{SELECTION_TYPE}/{SELECT_YEAR}/{SELECTION_TYPE}_data_{SELECT_YEAR}.json"
    # Load match data
    with open(match_data_file, "r") as file:
        data = json.load(file)[f"{SELECTION_TYPE}"]
    years_arr = {SELECT_YEAR: data[0][str(SELECT_YEAR)]}
    player_stats = {"PlayerDetailedStats": [{str(SELECT_YEAR): []}]}
    driver = set_up_driver()
    for year in [SELECT_YEAR]:
        try:
            for round in range(SELECT_ROUND):
                round_data = years_arr[year][round][str(round + 1)]
                round_results = []
                for game in round_data:
                    h_team, a_team = [game[x].replace(" ", "-") for x in ["Home", "Away"]]
                    match_key = f"{year}-{round+1}-{h_team}-v-{a_team}"
                    url = f"{WEBSITE}{year}/round-{round+1}/{h_team}-v-{a_team}/"
                    print(f"Fetching: {url}")
                    driver.get(url)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Extract advanced player data (example: add more selectors as needed)
                    rows = soup.find_all("tr", class_="table-tbody__tr")
                    players_info = []
                    for row in rows:
                        player_info = {}
                        player_name_elem = row.find("a", class_="table__content-link")
                        if player_name_elem:
                            player_info["Name"] = player_name_elem.get_text(strip=True, separator=" ")
                        statistics = row.find_all("td", class_="table__cell table-tbody__td")
                        for i, label in enumerate(EV.PLAYER_LABELS):
                            player_info[label] = statistics[i].get_text(strip=True) if i < len(statistics) else "na"
                        # Example: extract extra advanced stats (add selectors as needed)
                        # player_info["AdvancedStat"] = ...
                        players_info.append(player_info)
                    round_results.append({match_key: players_info})
                    print(f"Processed match: {match_key}")
                year_index = 0
                player_stats["PlayerDetailedStats"][year_index][str(year)].append({str(round): round_results})
                with open(player_stats_file, "w") as file:
                    json.dump(player_stats, file, indent=4)
                print(f"✅ Round {round+1} detailed player data saved.")
        except Exception as ex:
            print(f"Error: {ex}")
    driver.quit()
    print(f"Final detailed player statistics saved to {player_stats_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NRL Detailed Player Stats Scraper")
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--round', type=int, required=True)
    parser.add_argument('--type', type=str, default='NRL')
    args = parser.parse_args()
    player_data_detailed_select(args.year, args.round, args.type)
