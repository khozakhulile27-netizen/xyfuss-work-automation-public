# Xyfuss Work Automation

A public, carefully scoped portfolio snapshot of selected Xyfuss work-automation components.

Xyfuss is an experimental Python project exploring evidence-aware work intake, opportunity classification, requirement analysis, execution coordination, and delivery verification.

## What this snapshot demonstrates

- **Work opportunity lanes:** classifies observable opportunity text into coding, commerce, Xyfuss capability, or unknown.
- **Requirement verification:** compares a completed execution result with declared deliverables, output formats, and acceptance criteria.
- **Evidence-first design:** preserves unknowns instead of treating missing evidence as success.
- **Human approval boundaries:** work acceptance and consequential actions remain subject to owner authorization.

## Included source modules

- `core/work_opportunity_lane_classifier.py`
- `core/client_requirement_verifier.py`

These are selected components, not a complete runnable distribution of Xyfuss God Mode. The original repository, its runtime state, private data, backups, logs, and full development history are not included.

## Current limitations

- Opportunity lane classification is a text heuristic, not a legitimacy check or a guarantee of skill fit.
- Requirement verification checks supplied execution evidence; it does not independently prove that a file or service is correct.
- This snapshot does not autonomously apply for jobs, contact clients, accept contracts, spend money, or process payments.
- No claim is made that this portfolio snapshot is production-ready.

## Design principles

Observe → Understand → Evidence → Unknowns → Explain → Confidence → Recommend → Verify → Learn.

Truth before assumptions. Evidence before conclusions. Safety before action. Human authorization before consequential commitments.

## Technology

Python. The included modules use the Python standard library.

## Project status

Experimental / in development. Features and limitations are documented conservatively; only the files in this repository are part of this public snapshot.
