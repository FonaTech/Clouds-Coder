import unittest

from Clouds_Coder import SessionState


class PlanStructureTests(unittest.TestCase):
    def test_zero_prefixed_numeric_range_stays_in_previous_step(self):
        raw_steps = [
            "1. Initialization\n1.1 Create the project",
            "2. Computation\n2.1 Build the model",
            "3. Dense grid\n3.1 Create the frequency grid",
            "0. THz-750 THz, EF 0-0.5 eV\n0.1 THz-750 THz, EF 0-0.5 eV",
            "4. Report\n4.1 Render the result",
        ]

        grouped = SessionState._group_plan_steps(raw_steps)

        self.assertEqual(len(grouped), 4)
        self.assertIn("0. THz-750 THz", grouped[2])
        self.assertIn("0.1 THz-750 THz", grouped[2])
        self.assertTrue(grouped[3].startswith("4. Report"))

    def test_phase_hint_does_not_classify_paths_or_prose(self):
        instance = SessionState.__new__(SessionState)

        self.assertEqual(
            instance._plan_step_phase_hint(
                "Create src/tests/physics.py and run pytest"
            ),
            "",
        )


if __name__ == "__main__":
    unittest.main()
