"""Verify completed work against client-specific requirements."""

from __future__ import annotations


class ClientRequirementVerifier:
    """Compare a requirement specification with actual execution evidence."""

    VERSION = "1.0"

    @staticmethod
    def _require_dict(value, name):
        if not isinstance(value, dict):
            raise ValueError(f"{name} must be a dictionary.")

    @staticmethod
    def _normalize(value):
        return str(value).strip().lower()

    @classmethod
    def _deliverable_aliases(cls, requirement):
        """Return conservative canonical names for known deliverable wording."""
        normalized = cls._normalize(requirement)

        aliases = {
            "cleaned csv file": "cleaned dataset",
            "a cleaned csv file": "cleaned dataset",
            "clean csv file": "cleaned dataset",
            "a clean csv file": "cleaned dataset",
            "cleaned csv": "cleaned dataset",
            "a cleaned dataset": "cleaned dataset",
            "data quality report": "data quality report",
            "a data quality report": "data quality report",
        }

        return aliases.get(normalized, normalized)

    @classmethod
    def _check_deliverables(cls, specification, execution_result):
        required = specification.get("required_deliverables", [])
        if not isinstance(required, list):
            raise ValueError(
                "Requirement specification deliverables must be a list."
            )

        checks = []

        native_artifacts = {
            "cleaned dataset": execution_result.get("output_path"),
            "data quality report": execution_result.get("report_path"),
        }

        for requirement in required:
            if not isinstance(requirement, str) or not requirement.strip():
                raise ValueError(
                    "Requirement specification contains an invalid "
                    "deliverable."
                )

            parts = [
                part.strip()
                for part in requirement.split(" and ")
                if part.strip()
            ]

            matched_values = {}
            missing_parts = []

            for part in parts:
                requirement_key = cls._deliverable_aliases(part)
                matched_value = None

                for key, value in execution_result.items():
                    if cls._deliverable_aliases(key) == requirement_key:
                        matched_value = value
                        break

                if matched_value is None:
                    matched_value = native_artifacts.get(requirement_key)

                if matched_value is None:
                    missing_parts.append(part)
                else:
                    matched_values[part] = matched_value

            if missing_parts:
                checks.append(
                    {
                        "requirement": requirement,
                        "status": "unknown",
                        "evidence": matched_values or None,
                        "reason": (
                            "No matching execution deliverable was found "
                            "for: " + ", ".join(missing_parts)
                        ),
                    }
                )
                continue

            matched_value = (
                next(iter(matched_values.values()))
                if len(matched_values) == 1
                else matched_values
            )

            if isinstance(matched_value, str) and not matched_value.strip():
                checks.append(
                    {
                        "requirement": requirement,
                        "status": "failed",
                        "evidence": matched_value,
                        "reason": "The execution deliverable is empty.",
                    }
                )
                continue

            checks.append(
                {
                    "requirement": requirement,
                    "status": "satisfied",
                    "evidence": matched_value,
                }
            )

        return checks

    @classmethod
    def _check_output_format(cls, specification, execution_result):
        formats = specification.get("output_format", [])
        if not isinstance(formats, list):
            raise ValueError(
                "Requirement specification output_format must be a list."
            )

        if not formats:
            return {
                "status": "not_applicable",
                "requirement": None,
                "evidence": None,
                "reason": "No explicit output format was required.",
            }

        actual_format = execution_result.get("output_format")
        if actual_format is None:
            output_path = execution_result.get("output_path")
            if isinstance(output_path, str) and "." in output_path:
                actual_format = output_path.rsplit(".", 1)[-1].strip()

        if actual_format is None:
            return {
                "status": "unknown",
                "requirement": formats,
                "evidence": None,
                "reason": "Execution did not declare an output format.",
            }

        expected = {cls._normalize(value) for value in formats}
        actual = cls._normalize(actual_format)

        return {
            "status": "satisfied" if actual in expected else "failed",
            "requirement": formats,
            "evidence": actual_format,
        }

    @classmethod
    def _check_acceptance_criteria(cls, specification, execution_result):
        criteria = specification.get("acceptance_criteria", [])
        if not isinstance(criteria, list):
            raise ValueError(
                "Requirement specification acceptance criteria must be a list."
            )

        if not criteria:
            return []

        summary = execution_result.get("summary", {})
        if not isinstance(summary, dict):
            summary = {}

        results = []
        for criterion in criteria:
            if not isinstance(criterion, str) or not criterion.strip():
                raise ValueError(
                    "Requirement specification contains an invalid "
                    "acceptance criterion."
                )

            criterion_key = cls._normalize(criterion)
            normalized_summary = {
                cls._normalize(key): value
                for key, value in summary.items()
            }

            if criterion_key in normalized_summary:
                value = normalized_summary[criterion_key]
                results.append(
                    {
                        "requirement": criterion,
                        "status": (
                            "satisfied"
                            if value is True
                            else "failed"
                            if value is False
                            else "unknown"
                        ),
                        "evidence": value,
                    }
                )
            elif (
                criterion_key == "all records must be valid"
                and "validation_passed" in normalized_summary
            ):
                value = normalized_summary["validation_passed"]
                results.append(
                    {
                        "requirement": criterion,
                        "status": (
                            "satisfied"
                            if value is True
                            else "failed"
                            if value is False
                            else "unknown"
                        ),
                        "evidence": value,
                    }
                )
            else:
                results.append(
                    {
                        "requirement": criterion,
                        "status": "unknown",
                        "evidence": None,
                        "reason": (
                            "No explicit execution evidence was found "
                            "for this acceptance criterion."
                        ),
                    }
                )

        return results

    @classmethod
    def verify(cls, opportunity, execution, requirement_specification):
        """Verify client-specific requirements without changing lifecycle state."""

        cls._require_dict(opportunity, "Opportunity")
        cls._require_dict(execution, "Execution")
        cls._require_dict(
            requirement_specification,
            "Requirement specification",
        )

        opportunity_id = str(
            opportunity.get("opportunity_id", "")
        ).strip()
        if not opportunity_id:
            raise ValueError("Opportunity ID is required.")

        if execution.get("opportunity_id") != opportunity_id:
            raise ValueError("Execution opportunity ID does not match.")

        if execution.get("status") != "completed":
            raise ValueError(
                "Execution must be completed before requirement verification."
            )

        execution_result = execution.get("result")
        if not isinstance(execution_result, dict):
            raise ValueError("Execution result is required.")

        deliverable_checks = cls._check_deliverables(
            requirement_specification,
            execution_result,
        )
        output_format_check = cls._check_output_format(
            requirement_specification,
            execution_result,
        )
        acceptance_checks = cls._check_acceptance_criteria(
            requirement_specification,
            execution_result,
        )

        checks = {
            "deliverables": deliverable_checks,
            "output_format": output_format_check,
            "acceptance_criteria": acceptance_checks,
        }

        all_checks = deliverable_checks + [output_format_check] + acceptance_checks
        failed = [
            check
            for check in all_checks
            if check.get("status") == "failed"
        ]
        unknown = [
            check
            for check in all_checks
            if check.get("status") == "unknown"
        ]

        if failed:
            status = "failed"
        elif unknown:
            status = "needs_clarification"
        else:
            status = "satisfied"

        return {
            "contract_version": cls.VERSION,
            "verified": status == "satisfied",
            "status": status,
            "opportunity_id": opportunity_id,
            "checks": checks,
        }
