class WorkOpportunityLaneClassifier:
    """
    Evidence-based classification of work opportunities into Xyfuss lanes.

    Lanes:
    - commerce
    - coding
    - xyfuss_capability
    - unknown

    This classifier:
    - uses only observable opportunity information
    - does not search the web
    - does not collect pages
    - does not assess legitimacy
    - does not claim capability matches
    - does not apply, contact, spend, register, or execute
    """

    VERSION = 1

    VALID_LANES = {
        "commerce",
        "coding",
        "xyfuss_capability",
        "unknown",
    }

    CODING_TERMS = {
        "software development",
        "software developer",
        "software engineer",
        "web development",
        "web developer",
        "frontend",
        "backend",
        "full stack",
        "full-stack",
        "python",
        "javascript",
        "typescript",
        "java",
        "c++",
        "programming",
        "programmer",
        "developer",
        "coding",
        "api development",
        "mobile app development",
    }

    COMMERCE_TERMS = {
        "affiliate",
        "affiliate marketing",
        "ecommerce",
        "e-commerce",
        "online store",
        "product listing",
        "product sales",
        "sales commission",
        "commission",
        "advertising",
        "lead generation",
        "digital product",
        "sell products",
    }

    XYFUSS_CAPABILITY_TERMS = {
        "data cleaning",
        "data cleansing",
        "data validation",
        "data verification",
        "data quality",
        "data analysis",
        "data management",
        "data mining",
        "data entry",
        "dataset cleaning",
        "dataset cleansing",
        "dataset validation",
        "data reconciliation",
        "anomaly detection",
        "spreadsheet",
        "csv",
        "excel",
    }

    @staticmethod
    def _text(value):
        if value is None:
            return ""
        return str(value).strip().lower()

    @classmethod
    def _combined_text(cls, opportunity):
        if not isinstance(opportunity, dict):
            return ""

        parts = [
            opportunity.get("title"),
            opportunity.get("description"),
            opportunity.get("category"),
            opportunity.get("content"),
        ]

        metadata = opportunity.get("metadata", {})
        if isinstance(metadata, dict):
            parts.append(metadata.get("content"))

        skills = opportunity.get("skills", [])
        if isinstance(skills, list):
            parts.extend(skills)

        return " ".join(
            cls._text(part)
            for part in parts
            if cls._text(part)
        )

    @staticmethod
    def _matches(text, terms):
        return sorted(
            term
            for term in terms
            if term in text
        )

    @classmethod
    def classify(cls, opportunity):
        """
        Classify an opportunity using observable text.

        Returns:
            {
                "lane": "...",
                "confidence": "...",
                "evidence": [...]
            }

        Ambiguous or weak evidence returns "unknown".
        """
        text = cls._combined_text(opportunity)

        if not text:
            return {
                "lane": "unknown",
                "confidence": "low",
                "evidence": [],
            }

        coding_matches = cls._matches(
            text,
            cls.CODING_TERMS,
        )
        commerce_matches = cls._matches(
            text,
            cls.COMMERCE_TERMS,
        )
        capability_matches = cls._matches(
            text,
            cls.XYFUSS_CAPABILITY_TERMS,
        )

        scores = {
            "coding": len(coding_matches),
            "commerce": len(commerce_matches),
            "xyfuss_capability": len(capability_matches),
        }

        ordered = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        best_lane, best_score = ordered[0]
        second_score = ordered[1][1]

        if best_score == 0:
            lane = "unknown"
            confidence = "low"
        elif best_score == second_score:
            lane = "unknown"
            confidence = "low"
        elif best_score == 1:
            lane = best_lane
            confidence = "low"
        else:
            lane = best_lane
            confidence = "medium"

        evidence = {
            "coding": coding_matches,
            "commerce": commerce_matches,
            "xyfuss_capability": capability_matches,
        }

        return {
            "lane": lane,
            "confidence": confidence,
            "evidence": evidence,
            "scores": scores,
        }

    def status(self):
        return {
            "version": self.VERSION,
            "status": "ready",
            "lanes": sorted(self.VALID_LANES),
        }
