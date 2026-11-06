import json
import os
import tempfile
from pathlib import Path


DEFAULT_FILE = Path("tournament.json")


def validate_tournament_data(data):

    if not isinstance(data, dict):
        raise ValueError("Tournament data must be a dictionary.")

    if "teams" not in data or "fixtures" not in data:
        raise ValueError("Tournament data must contain teams and fixtures.")

    if not isinstance(data["teams"], list):
        raise ValueError("Teams must be stored as a list.")

    if not isinstance(data["fixtures"], list):
        raise ValueError("Fixtures must be stored as a list.")

    if not all(isinstance(team, dict) for team in data["teams"]):
        raise ValueError("Every team must be a dictionary.")

    if not all(isinstance(fixture, dict) for fixture in data["fixtures"]):
        raise ValueError("Every fixture must be a dictionary.")

    if "name" in data and not isinstance(data["name"], str):
        raise ValueError("Tournament name must be text.")

    return True


def save_tournament(
    teams,
    fixtures,
    file_path=DEFAULT_FILE,
    tournament_name=None
):

    data = {
        "teams": teams,
        "fixtures": fixtures
    }

    if tournament_name is not None:
        data["name"] = tournament_name

    validate_tournament_data(data)

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=file_path.parent,
            delete=False,
            suffix=".tmp"
        ) as temporary_file:

            json.dump(data, temporary_file, indent=4)
            temporary_path = Path(temporary_file.name)

        os.replace(temporary_path, file_path)

    except (TypeError, OSError):
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()

        raise

    return True


def load_tournament(file_path=DEFAULT_FILE):

    file_path = Path(file_path)

    if not file_path.exists():
        return None

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Tournament file contains invalid JSON."
        ) from error

    except OSError as error:
        raise OSError(
            "Unable to read tournament file."
        ) from error

    validate_tournament_data(data)

    return data


def initialize_tournament(file_path=DEFAULT_FILE):

    existing_data = load_tournament(file_path)

    if existing_data is not None:
        return existing_data

    empty_tournament = {
        "teams": [],
        "fixtures": []
    }

    save_tournament(
        empty_tournament["teams"],
        empty_tournament["fixtures"],
        file_path
    )

    return empty_tournament