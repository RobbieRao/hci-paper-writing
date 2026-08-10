# Security and manuscript privacy

## Supported version

Security and privacy fixes target the latest release on the default branch.

## Report a vulnerability

Use GitHub's private vulnerability reporting feature when available. Do not open
a public issue containing an unpublished manuscript, credentials, personal data,
or a working exploit.

## Data boundary

The bundled `manuscript_audit.py` script performs a local, read-only scan and
makes no network requests. The agent skill itself is instruction text. Data
handling by the model or application running the skill is governed by that
platform, not by this repository.

Users are responsible for confirming that they are authorized to process a
manuscript and that their chosen AI platform satisfies applicable confidentiality
and venue requirements.

