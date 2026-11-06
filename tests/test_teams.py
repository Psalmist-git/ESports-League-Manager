import unittest

from tournament.teams import (
    register_team,
    validate_teams,
    create_npfl_teams,
    NPFL_TEAMS
)


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_register_valid_team(self):
        team = register_team(self.teams, "Enugu Rangers")

        self.assertEqual(team["id"], "T001")
        self.assertEqual(team["name"], "Enugu Rangers")
        self.assertEqual(len(self.teams), 1)

    def test_reject_empty_team_name(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "")

    def test_reject_duplicate_team_name(self):
        register_team(self.teams, "Enugu Rangers")

        with self.assertRaises(ValueError):
            register_team(self.teams, "enugu rangers")

    def test_reject_ninth_team(self):
        for name in NPFL_TEAMS:
            register_team(self.teams, name)

        with self.assertRaises(ValueError):
            register_team(self.teams, "New Football Club")

    def test_reject_fewer_than_four_teams(self):
        register_team(self.teams, "Enugu Rangers")
        register_team(self.teams, "Enyimba FC")

        with self.assertRaises(ValueError):
            validate_teams(self.teams)

    def test_register_eight_npfl_teams(self):
        teams = create_npfl_teams()

        self.assertEqual(len(teams), 8)
        self.assertTrue(validate_teams(teams))


if __name__ == "__main__":
    unittest.main()