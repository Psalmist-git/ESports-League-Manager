def record_result(fixtures, fixture_id, home_score, away_score):

    # 1. Validate score data types.
    if type(home_score) is not int or type(away_score) is not int:
        raise ValueError("Scores must be integers.")

    # 2. Reject negative scores.
    if home_score < 0 or away_score < 0:
        raise ValueError("Scores cannot be negative.")

    # 3. Find the requested fixture.
    matching_fixtures = [
        fixture for fixture in fixtures
        if fixture["fixture_id"] == fixture_id
    ]

    if not matching_fixtures:
        raise ValueError("Fixture ID does not exist.")

    # 4. Ensure fixture IDs are unique.
    if len(matching_fixtures) > 1:
        raise ValueError("Duplicate fixture IDs detected.")

    fixture = matching_fixtures[0]

    # 5. Prevent duplicate result submissions.
    if fixture["played"]:
        raise ValueError("This fixture has already been played.")

    # 6. Record the result.
    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["played"] = True

    return fixture