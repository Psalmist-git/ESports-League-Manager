def generate_fixtures(teams):

    if not 4 <= len(teams) <= 8:
        raise ValueError("Tournament requires 4 to 8 teams.")

    team_ids = [team["id"] for team in teams]

    if len(team_ids) != len(set(team_ids)):
        raise ValueError("Duplicate team IDs detected.")

    rotation = teams.copy()

    fixtures = []
    fixture_number = 1

    total_rounds = len(rotation) - 1

    for round_number in range(1, total_rounds + 1):

        for i in range(len(rotation) // 2):

            home_team = rotation[i]
            away_team = rotation[-(i + 1)]

            fixture = {
                "fixture_id": f"F{fixture_number:03d}",
                "round": round_number,
                "home_team_id": home_team["id"],
                "away_team_id": away_team["id"],
                "home_team": home_team["name"],
                "away_team": away_team["name"],
                "home_score": None,
                "away_score": None,
                "played": False
            }

            fixtures.append(fixture)

            fixture_number += 1

        # Keep the first team fixed and rotate the others.
        rotation = [
            rotation[0],
            rotation[-1],
            *rotation[1:-1]
        ]

    return fixtures