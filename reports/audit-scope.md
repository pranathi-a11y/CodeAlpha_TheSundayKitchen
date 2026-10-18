# Secure Coding Review — Audit Scope

**Project:** The Sunday Kitchen — Culinary Studio  
**Review date:** 2026-10-18  
**Reviewer:** CodeAlpha Cyber Security Internship Task 3

## Environment and evidence

| Item | Observed value |
|---|---|
| Runtime used for this review | Python 3.8.5 (`.venv/bin/python`) |
| Flask | 3.0.3 |
| Flask-WTF | 1.2.1 |
| pytest | 8.3.5 |
| Bandit actually run | 1.7.10 |
| Database | SQLite via Python stdlib |

Commands run after the implementation changes:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m bandit -r app.py catalog.py -ll -f txt
```

The second command’s unmodified output is saved in `reports/bandit-output.txt`.

## Files and controls reviewed

- Flask routes, database helpers, input validation and error handling in `app.py`.
- Catalogue data and asset paths in `catalog.py`.
- All Jinja templates, including the contact-success dialog and both POST forms.
- `static/css/styles.css` and `static/js/main.js` for the changed UI interactions.
- Tests in `tests/test_app.py`.
- Dependency bounds and the security-report artefacts.

The review verifies CSRF on POST routes, server-side validation, workshop/session allowlists, parameterized SQLite statements, Jinja autoescaping, production secret-key safeguards, session cookie flags, request-size limits, controlled error responses, and HTTP response headers including CSP.

## Scope limitations

- This is a local review, not a production deployment or penetration test. TLS, reverse proxy configuration, backup, monitoring and production rate limiting were not tested.
- No email sending, payments, booking confirmation or availability system exists. A contact acknowledgement means only that a local SQLite save completed.
- The in-app browser was unavailable in this environment, so responsive visual checks were limited to template/CSS inspection, Flask test-client route checks and static-asset HTTP checks.
- External Google Fonts and the remaining Unsplash imagery on the journal/studio sections were not assessed for availability, privacy or licensing.
- Tests and static analysis improve confidence but do not prove that the application is free of all security defects.

## Bandit version correction

A previous report incorrectly stated that Bandit 1.8.x did not exist. PyPI publishes Bandit 1.8.0 and later 1.8.x releases; Bandit 1.8.0 declares `Requires-Python: >=3.9`. The recorded Python 3.8.5 environment therefore correctly uses Bandit 1.7.10, whose PyPI metadata declares `Requires-Python: >=3.8`. The requirements file uses Python-version markers so each supported interpreter selects a compatible Bandit series.
