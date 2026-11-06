def calculate_standings(teams, fixtures):

    # Create an initial league record for every team.
    standings = {}

    for team in teams:
        team_id = team["id"]

        if team_id in standings:
            raise ValueError("Duplicate team IDs detected.")

        standings[team_id] = {
            "team_id": team_id,
            "team": team["name"],
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    # Process completed fixtures only.
    for fixture in fixtures:

        if not fixture["played"]:
            continue

        home_id = fixture["home_team_id"]
        away_id = fixture["away_team_id"]

        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        # Validate fixture participants.
        if home_id not in standings or away_id not in standings:
            raise ValueError("Fixture contains an unknown team ID.")

        if home_id == away_id:
            raise ValueError("A team cannot play against itself.")

        # Validate recorded scores.
        if (
            type(home_score) is not int
            or type(away_score) is not int
            or home_score < 0
            or away_score < 0
        ):
            raise ValueError("Invalid match scores.")

        home = standings[home_id]
        away = standings[away_id]

        # Update matches played.
        home["played"] += 1
        away["played"] += 1

        # Update goals scored and conceded.
        home["goals_for"] += home_score
        home["goals_against"] += away_score

        away["goals_for"] += away_score
        away["goals_against"] += home_score

        # Determine match outcome.
        if home_score > away_score:

            home["won"] += 1
            away["lost"] += 1

            home["points"] += 3

        elif home_score < away_score:

            away["won"] += 1
            home["lost"] += 1

            away["points"] += 3

        else:

            home["drawn"] += 1
            away["drawn"] += 1

            home["points"] += 1
            away["points"] += 1

    # Calculate goal difference.
    for team in standings.values():

        team["goal_difference"] = (
            team["goals_for"] - team["goals_against"]
        )

    # Apply tournament ranking rules.
    sorted_standings = sorted(
        standings.values(),
        key=lambda team: (
            -team["points"],
            -team["goal_difference"],
            -team["goals_for"],
            " ".join(team["team"].split()).casefold()
        )
    )

    # Assign league positions.
    for position, team in enumerate(sorted_standings, start=1):
        team["position"] = position

    return sorted_standings