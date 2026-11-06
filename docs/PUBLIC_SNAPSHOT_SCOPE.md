# Public Snapshot: Scope and Safety

## Purpose

This repository publishes a small, reviewable subset of Xyfuss work-automation code for portfolio evaluation. It is intentionally separate from the private development repository.

## Included

- A keyword-based opportunity lane classifier.
- A client-requirement verifier that reports satisfied, failed, or unknown checks based on supplied execution evidence.

## Excluded

This public snapshot does not contain:

- Runtime databases, memory, audit logs, task state, or financial records.
- Customer or lead records, even if sample-looking.
- Backups, local configuration, environment files, API keys, tokens, passwords, or provider credentials.
- Private repository history or unrelated project files.
- Executable integrations that contact employers, clients, brokers, or payment providers.

## Safety boundaries

Classification is not a legitimacy assessment. A classification result must not be treated as permission to apply, contact a person, accept work, sign an agreement, spend money, or make a financial commitment.

Requirement verification is only as reliable as the execution evidence supplied to it. Missing evidence is reported as unknown rather than silently treated as success.

## Status and verification

This is a selected source snapshot, not the complete Xyfuss application. It has not been represented as a complete installable product or independently re-tested as a standalone package in this repository.
