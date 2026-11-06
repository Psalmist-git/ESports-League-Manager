import random

from tournament.results import record_result


def simulate_tournament(fixtures, confirmed=False):

    # Require explicit confirmation.
    if confirmed is not True:
        raise PermissionError(
            "Simulation requires explicit confirmation."
        )

    simulated_count = 0

    for fixture in fixtures:

        # Preserve previously recorded results.
        if fixture["played"]:
            continue

        # Generate random football scores between 0 and 15.
        home_score = random.randint(0, 15)
        away_score = random.randint(0, 15)

        # Record the result using the existing result manager.
        record_result(
            fixtures,
            fixture["fixture_id"],
            home_score,
            away_score
        )

        simulated_count += 1

    return {
        "fixtures": fixtures,
        "simulated_matches": simulated_count
    }