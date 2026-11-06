import unittest

from core.client_requirement_verifier import ClientRequirementVerifier
from core.work_opportunity_lane_classifier import WorkOpportunityLaneClassifier


class WorkOpportunityLaneClassifierTests(unittest.TestCase):
    def test_coding_opportunity_is_classified(self):
        result = WorkOpportunityLaneClassifier.classify({
            "title": "Python software development",
            "description": "Build a Python API",
        })
        self.assertEqual(result["lane"], "coding")
        self.assertIn(result["confidence"], {"low", "medium"})

    def test_ambiguous_opportunity_stays_unknown(self):
        result = WorkOpportunityLaneClassifier.classify({
            "title": "General opportunity",
            "description": "Something interesting",
        })
        self.assertEqual(result["lane"], "unknown")


class ClientRequirementVerifierTests(unittest.TestCase):
    def test_matching_execution_evidence_satisfies_requirements(self):
        result = ClientRequirementVerifier.verify(
            opportunity={"opportunity_id": "OPP-TEST"},
            execution={
                "opportunity_id": "OPP-TEST",
                "status": "completed",
                "result": {
                    "output_path": "cleaned.csv",
                    "output_format": "csv",
                    "summary": {"all records must be valid": True},
                },
            },
            requirement_specification={
                "required_deliverables": ["cleaned CSV file"],
                "output_format": ["csv"],
                "acceptance_criteria": ["all records must be valid"],
            },
        )
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"], "satisfied")

    def test_missing_evidence_is_not_treated_as_success(self):
        result = ClientRequirementVerifier.verify(
            opportunity={"opportunity_id": "OPP-TEST"},
            execution={
                "opportunity_id": "OPP-TEST",
                "status": "completed",
                "result": {},
            },
            requirement_specification={
                "required_deliverables": ["cleaned CSV file"],
                "output_format": ["csv"],
                "acceptance_criteria": ["all records must be valid"],
            },
        )
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "needs_clarification")


if __name__ == "__main__":
    unittest.main()
