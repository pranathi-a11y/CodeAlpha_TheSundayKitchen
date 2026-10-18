# Remediation & Validation Report

**Project:** The Sunday Kitchen — Culinary Studio  
**Review date:** 2026-10-18  
**Reviewer:** CodeAlpha Cyber Security Internship Task 3

## Completed implementation work

- Replaced all public fictional instructor references with Pranathi Chaliseemala, Prakruti B and Amrutha Gowda, in that order, using their supplied local photographs.
- Created and used `amrutha-upright.jpg`, a 90° counter-clockwise display derivative of the supplied Amrutha photograph; the original `amrutha.jpg` remains unchanged.
- Replaced workshop CDN image usage with local files. The original sourdough Unsplash URL returned HTTP 404; a verified sourdough image is now served locally as `static/images/workshops/sourdough-sunday.jpg`.
- Updated contact details and introduced an accessible native-dialog acknowledgement that appears only after a successful SQLite commit.
- Added controlled SQLite failure handling for contact saves. It returns a generic error and does not show the acknowledgement.
- Removed public-facing placeholder and fictional-profile warnings, and removed unused root-level standalone `index.html`, `styles.css` and empty `package-lock.json` files after confirming the Flask app does not reference them.

## Bandit correction and dependency policy

The former statement that “Bandit 1.8.x does not exist” was incorrect.

| Version | PyPI metadata | Relevance |
|---|---|---|
| Bandit 1.7.10 | `Requires-Python: >=3.8` | Actually used by the recorded and current review environment (Python 3.8.5). |
| Bandit 1.8.0 | `Requires-Python: >=3.9` | A real release, but incompatible with Python 3.8.5. |

`requirements.txt` now selects `>=1.7,<1.8` on Python < 3.9 and `>=1.8,<2.0` on Python 3.9+. This distinguishes the version actually tested from newer supported releases instead of claiming newer releases are unavailable.

Source: [Bandit 1.7.10 PyPI metadata](https://pypi.org/project/bandit/1.7.10/) and [Bandit 1.8.0 PyPI metadata](https://pypi.org/project/bandit/1.8.0/).

## Validation results

| Check | Result |
|---|---|
| `.venv/bin/python -m pytest -q` | 27 passed, 0 failed |
| `.venv/bin/python -m bandit -r app.py catalog.py -ll -f txt` | Exit 0; no issues identified; output saved in `reports/bandit-output.txt` |
| Local workshop/instructor static-asset tests | All requested paths return `image/jpeg` |
| Contact-save integration test | Valid CSRF-protected submission persists and renders the acknowledgement |
| Failure-path tests | Validation, missing CSRF and simulated SQLite errors never render the acknowledgement |

## Remaining limitations

The application has no email delivery, payment workflow, rate limiting, production data-retention mechanism, authenticated admin interface or deployed-environment test. None of those are claimed as completed by this report.
