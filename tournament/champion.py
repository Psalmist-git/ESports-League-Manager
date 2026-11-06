from tournament.standings import calculate_standings


def declare_champion(teams, fixtures):

    # 1. Confirm the tournament has a valid number of teams.
    if not 4 <= len(teams) <= 8:
        raise ValueError("Tournament requires 4 to 8 teams.")

    # 2. Calculate how many fixtures a round-robin tournament requires.
    expected_fixtures = len(teams) * (len(teams) - 1) // 2

    # 3. Ensure all expected fixtures exist.
    if len(fixtures) != expected_fixtures:
        raise ValueError(
            "Cannot declare champion: fixture schedule is incomplete."
        )

    # 4. Ensure every fixture has been played.
    unplayed_fixtures = [
        fixture for fixture in fixtures
        if fixture["played"] is not True
    ]

    if unplayed_fixtures:
        raise ValueError(
            f"Cannot declare champion: "
            f"{len(unplayed_fixtures)} fixture(s) remain unplayed."
        )

    # 5. Calculate the final league standings.
    standings = calculate_standings(teams, fixtures)

    # 6. The first team in the sorted standings is champion.
    champion = standings[0]

    # 7. Return the champion and final standings.
    return {
        "champion": champion,
        "standings": standings,
        "total_fixtures": expected_fixtures,
        "completed_fixtures": len(fixtures)
    }