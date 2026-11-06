import re
from pathlib import Path

from tournament.teams import create_npfl_teams
from tournament.fixtures import generate_fixtures
from tournament.results import record_result
from tournament.standings import calculate_standings
from tournament.storage import load_tournament, save_tournament
from tournament.simulation import simulate_tournament
from tournament.champion import declare_champion


TOURNAMENTS_DIR = Path("tournaments")


def create_file_name(name):

    slug = re.sub(r"[^a-z0-9]+", "-", name.casefold())
    return slug.strip("-") + ".json"


def list_saved_tournaments():

    TOURNAMENTS_DIR.mkdir(parents=True, exist_ok=True)

    saved_tournaments = []

    for file_path in sorted(TOURNAMENTS_DIR.glob("*.json")):

        try:
            data = load_tournament(file_path)

            if data is None:
                continue

            name = data.get(
                "name",
                file_path.stem.replace("-", " ").title()
            )
            data["name"] = name

            saved_tournaments.append({
                "name": name,
                "path": file_path,
                "data": data
            })

        except (ValueError, OSError) as error:
            print(
                f"\nWarning: Could not load "
                f"{file_path.name}: {error}"
            )

    return saved_tournaments


def save_active_tournament(data, file_path):

    save_tournament(
        data["teams"],
        data["fixtures"],
        file_path,
        tournament_name=data["name"]
    )


def create_new_tournament():

    print("\nCREATE A NEW TOURNAMENT")
    print("-" * 40)

    name = input("Enter tournament name: ").strip()


    file_name = create_file_name(name)
    if not name:
        print("\nTournament name cannot be empty.")
        return None
    
    if file_name == ".json":
        print("\nPlease use letters or numbers in the tournament name.")
        return None
    file_path = TOURNAMENTS_DIR / file_name

    existing_tournaments = list_saved_tournaments()

    for tournament in existing_tournaments:

        if tournament["name"].casefold() == name.casefold():
            print("\nA tournament with this name already exists.")
            print("Select the existing tournament instead.")
            return None

    if file_path.exists():
        print("\nA tournament file with this name already exists.")
        print("Choose another tournament name.")
        return None

    teams = create_npfl_teams()
    fixtures = generate_fixtures(teams)

    data = {
        "name": name,
        "teams": teams,
        "fixtures": fixtures
    }

    save_active_tournament(data, file_path)

    print("\nTournament successfully created!")
    print(f"Tournament name: {name}")
    print(f"Teams registered: {len(teams)}")
    print(f"Rounds: {len(teams) - 1}")
    print(f"Total fixtures: {len(fixtures)}")
    print(f"Saved as: {file_path}")

    return {
        "data": data,
        "path": file_path
    }


def select_tournament():

    while True:

        saved_tournaments = list_saved_tournaments()

        print("\n" + "=" * 45)
        print("          TOURNAMENTLAB")
        print("       TOURNAMENT MANAGER")
        print("=" * 45)

        if saved_tournaments:

            print("\nSAVED TOURNAMENTS")

            for number, tournament in enumerate(
                saved_tournaments,
                start=1
            ):
                print(f"{number}. {tournament['name']}")

        else:
            print("\nNo saved tournaments found.")

        print("\nN. Create a new tournament")
        print("Q. Exit")

        choice = input("\nSelect an option: ").strip().casefold()

        if choice == "q":
            return None

        if choice == "n":
            created = create_new_tournament()

            if created is not None:
                return created

        else:

            try:
                selection = int(choice)

                if 1 <= selection <= len(saved_tournaments):

                    selected = saved_tournaments[selection - 1]

                    print(
                        f"\nOpened tournament: "
                        f"{selected['name']}"
                    )

                    return {
                        "data": selected["data"],
                        "path": selected["path"]
                    }

                print("\nInvalid tournament selection.")

            except ValueError:
                print("\nEnter a valid number, N, or Q.")


def display_menu(tournament_name):

    print("\n" + "=" * 50)
    print("               TOURNAMENTLAB")
    print("=" * 50)
    print(f"ACTIVE TOURNAMENT: {tournament_name}")
    print("-" * 50)

    print("1. Switch/Create Tournament")
    print("2. View Fixtures")
    print("3. Record Match Result")
    print("4. View League Standings")
    print("5. Simulate Remaining Matches")
    print("6. Declare Champion")
    print("7. Exit")

    print("=" * 50)


def display_teams(teams):

    print("\nREGISTERED TEAMS")
    print("-" * 40)

    for number, team in enumerate(teams, start=1):
        print(f"{number}. {team['name']} ({team['id']})")


def display_fixtures(fixtures):

    if not fixtures:
        print("\nNo fixtures available.")
        return

    print("\nTOURNAMENT FIXTURES")
    print("-" * 65)

    for fixture in fixtures:

        if fixture["played"]:
            result = (
                f"{fixture['home_score']} - "
                f"{fixture['away_score']}"
            )
            status = "Played"

        else:
            result = "vs"
            status = "Pending"

        print(
            f"{fixture['fixture_id']} | "
            f"Round {fixture['round']} | "
            f"{fixture['home_team']} {result} "
            f"{fixture['away_team']} | {status}"
        )


def display_standings(teams, fixtures):

    if not teams or not fixtures:
        print("\nCreate a tournament first.")
        return

    standings = calculate_standings(teams, fixtures)

    print("\nLEAGUE STANDINGS")
    print("-" * 90)

    print(
        f"{'POS':<5}"
        f"{'TEAM':<30}"
        f"{'P':<5}"
        f"{'W':<5}"
        f"{'D':<5}"
        f"{'L':<5}"
        f"{'GF':<6}"
        f"{'GA':<6}"
        f"{'GD':<6}"
        f"{'PTS':<6}"
    )

    print("-" * 90)

    for team in standings:

        print(
            f"{team['position']:<5}"
            f"{team['team']:<30}"
            f"{team['played']:<5}"
            f"{team['won']:<5}"
            f"{team['drawn']:<5}"
            f"{team['lost']:<5}"
            f"{team['goals_for']:<6}"
            f"{team['goals_against']:<6}"
            f"{team['goal_difference']:<6}"
            f"{team['points']:<6}"
        )


def enter_match_result(data, file_path):

    if not data["fixtures"]:
        print("\nNo fixtures available.")
        return

    display_fixtures(data["fixtures"])

    fixture_id = input("\nEnter fixture ID: ").strip().upper()

    try:
        home_score = int(input("Enter home team score: "))
        away_score = int(input("Enter away team score: "))

        result = record_result(
            data["fixtures"],
            fixture_id,
            home_score,
            away_score
        )

        save_active_tournament(data, file_path)

        print("\nResult successfully recorded!")
        print(
            f"{result['home_team']} "
            f"{result['home_score']} - "
            f"{result['away_score']} "
            f"{result['away_team']}"
        )

    except ValueError as error:
        print(f"\nUnable to record result: {error}")


def run_simulation(data, file_path):

    if not data["fixtures"]:
        print("\nNo fixtures available.")
        return

    confirmation = input(
        "\nThis will generate random results for all remaining "
        "fixtures.\nType SIMULATE to continue: "
    ).strip()

    if confirmation != "SIMULATE":
        print("\nSimulation cancelled.")
        return

    try:
        result = simulate_tournament(
            data["fixtures"],
            confirmed=True
        )

        data["fixtures"] = result["fixtures"]

        save_active_tournament(data, file_path)

        print("\nSimulation completed!")
        print(
            f"Matches simulated: "
            f"{result['simulated_matches']}"
        )

    except (ValueError, PermissionError) as error:
        print(f"\nSimulation failed: {error}")


def show_champion(data):

    if not data["teams"]:
        print("\nNo tournament teams found.")
        return

    try:
        result = declare_champion(
            data["teams"],
            data["fixtures"]
        )

        champion = result["champion"]

        print("\n" + "=" * 45)
        print("          TOURNAMENT CHAMPION")
        print("=" * 45)

        print(f"\nCongratulations to {champion['team']}!")
        print(f"Total points: {champion['points']}")
        print(f"Matches played: {champion['played']}")
        print(f"Goal difference: {champion['goal_difference']}")

        print("\nFINAL LEAGUE TABLE")

        display_standings(
            data["teams"],
            data["fixtures"]
        )

    except (ValueError, IndexError) as error:
        print(f"\nChampion declaration unavailable: {error}")


def main():

    active_tournament = select_tournament()

    if active_tournament is None:
        print("\nTournamentLab closed. Goodbye!")
        return

    data = active_tournament["data"]
    file_path = active_tournament["path"]

    while True:

        display_menu(data["name"])

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":

            selected = select_tournament()

            if selected is not None:
                data = selected["data"]
                file_path = selected["path"]

        elif choice == "2":
            display_fixtures(data["fixtures"])

        elif choice == "3":
            enter_match_result(data, file_path)

        elif choice == "4":
            display_standings(data["teams"], data["fixtures"])

        elif choice == "5":
            run_simulation(data, file_path)

        elif choice == "6":
            show_champion(data)

        elif choice == "7":
            print("\nTournamentLab closed. Goodbye!")
            break

        else:
            print("\nInvalid selection. Choose a number from 1 to 7.")


if __name__ == "__main__":
    main()