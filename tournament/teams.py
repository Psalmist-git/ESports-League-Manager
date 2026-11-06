MIN_TEAMS = 4
MAX_TEAMS = 8

NPFL_TEAMS = [
    "Rangers International FC",
    "Enyimba FC",
    "Kano Pillars FC",
    "Rivers United FC",
    "Shooting Stars FC (3SC)",
    "Bendel Insurance FC",
    "Plateau United FC",
    "Ikorodu City FC"
]


def register_team(teams, name):

    name = " ".join(name.split())

    if not name:
        raise ValueError("Team name cannot be empty.")

    if len(teams) >= MAX_TEAMS:
        raise ValueError("Maximum of 8 teams allowed.")

    existing_names = [
        team["name"].casefold()
        for team in teams
    ]

    if name.casefold() in existing_names:
        raise ValueError("Team already registered.")

    team_id = f"T{len(teams) + 1:03d}"

    team = {
        "id": team_id,
        "name": name
    }

    teams.append(team)

    return team


def validate_teams(teams):

    if not MIN_TEAMS <= len(teams) <= MAX_TEAMS:
        raise ValueError("Tournament requires 4 to 8 teams.")

    team_ids = [team["id"] for team in teams]

    team_names = [
        team["name"].casefold()
        for team in teams
    ]

    if len(team_ids) != len(set(team_ids)):
        raise ValueError("Duplicate team IDs detected.")

    if len(team_names) != len(set(team_names)):
        raise ValueError("Duplicate team names detected.")

    return True


def create_npfl_teams():

    teams = []

    for name in NPFL_TEAMS:
        register_team(teams, name)

    validate_teams(teams)

    return teams