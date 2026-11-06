# TournamentLab
### NPFL Round-Robin Tournament Management System

TournamentLab is a Python command-line application for managing a round-robin football competition using Nigerian Professional Football League (NPFL) clubs.

The application allows users to register teams, generate fixtures, record match results, calculate league standings, simulate remaining matches, and declare a tournament champion.

## Features

- **Team Registration:** Supports 4–8 unique football teams.
- **Fixture Generation:** Automatically generates round-robin fixtures.
- **Match Management:** Records and validates match scores.
- **League Standings:** Calculates points, wins, draws, losses, goals scored, goals conceded, and goal difference.
- **Ranking System:** Uses points, goal difference, goals scored, and alphabetical team name as tie-breakers.
- **Data Persistence:** Saves tournament information in a JSON file.
- **Match Simulation:** Generates random results for remaining fixtures, but only after explicit user confirmation.
- **Champion Declaration:** Declares the champion only after every scheduled fixture has been played.

## Competition Format

The configured competition uses eight selected NPFL clubs.

- Teams: 8
- Rounds: 7
- Fixtures per round: 4
- Total fixtures: 28
- Matches per team: 7

This is a custom eight-team competition, not the official NPFL league season.

## Selected Teams

1. Rangers International FC
2. Enyimba FC
3. Kano Pillars FC
4. Rivers United FC
5. Shooting Stars Sports Club (3SC)
6. Bendel Insurance FC
7. Plateau United FC
8. Ikorodu City FC

## Points System

| Match Outcome | Points |
|---|---:|
| Win | 3 |
| Draw | 1 |
| Loss | 0 |

### Ranking and Tie-Breaking Rules

Teams are ranked using the following order:

1. Highest total points.
2. Highest goal difference.
3. Highest goals scored.
4. Alphabetical order of normalized team names.

## Project Structure

```text
TournamentLab/
│
├── main.py
├── tournament/
│   ├── __init__.py
│   ├── teams.py
│   ├── fixtures.py
│   ├── results.py
│   ├── standings.py
│   ├── storage.py
│   ├── simulation.py
│   └── champion.py
│
├── tests/
│   ├── __init__.py
│   └── test_teams.py
│
├── tournament.json
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or later.
- No external Python packages are required.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Enter the project directory

```bash
cd TournamentLab
```

### 3. Run the application

```bash
python main.py
```

## How to Use

When the application starts, a menu appears with the following options:

| Option | Action |
|---|---|
| 1 | Create Tournament |
| 2 | View Fixtures |
| 3 | Record Match Result |
| 4 | View League Standings |
| 5 | Simulate Remaining Matches |
| 6 | Declare Champion |
| 7 | Exit |

### Creating a Tournament

Select option 1 to register the eight configured teams and generate the complete fixture schedule.

### Recording Match Results

Select option 3, enter the fixture ID, and provide the home and away scores.

The application rejects invalid scores, unknown fixture IDs, and attempts to record a result for a fixture that has already been played.

### Viewing League Standings

Select option 4 to view the current league table. Only completed matches contribute to the standings.

### Simulating Matches

Select option 5 to simulate all remaining fixtures. The application requires the user to type `SIMULATE` before proceeding.

### Declaring the Champion

Select option 6 to declare the tournament champion. The application will reject the request if any scheduled fixture remains unplayed.

## Data Storage

Tournament information is stored in `tournament.json`.

The file contains:

- Registered teams.
- Generated fixtures.
- Match scores.
- Fixture completion status.

The application automatically saves changes so tournament progress can be continued in a later session.

## Running Tests

Run the available unit tests with:

```bash
python -m unittest discover -s tests -v
```

## Technologies

- Python
- JSON
- Python Standard Library
- unittest

## Project Goal

TournamentLab demonstrates practical Python programming concepts, including modular programming, functions, data validation, lists, dictionaries, file handling, JSON persistence, sorting, exception handling, and automated testing.