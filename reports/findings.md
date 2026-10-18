# Secure Coding Review — Findings Register

**Project:** The Sunday Kitchen — Culinary Studio  
**Review date:** 2026-10-18  
**Status:** Local implementation review complete

## Confirmed results

No medium- or high-severity Bandit findings were reported for the production sources (`app.py`, `catalog.py`) in the actual scan saved in `reports/bandit-output.txt`. Bandit 1.7.10 scanned 276 lines of code and reported zero issues at every severity level.

The current test suite contains 27 tests. The local run completed with **27 passed**.

## Verified controls

| Control | Evidence |
|---|---|
| CSRF protection | `CSRFProtect(app)` protects both POST routes; forms render `csrf_token`; tests reject missing tokens. |
| Server-side validation | Contact and booking inputs are length/format/control-character validated before persistence. |
| Allowlisted bookings | `/enquire` checks the workshop slug and verifies the selected session belongs to that workshop. |
| SQL injection resistance | Both inserts use SQLite parameter placeholders; values are never interpolated into SQL. |
| Template output encoding | Jinja autoescaping is retained; reflected XSS test passes. |
| Secret and cookie safeguards | Production refuses an unset `SECRET_KEY`; cookie HTTPOnly/SameSite/Secure settings are retained. |
| Request limit and controlled errors | 16 KiB request limit remains; contact SQLite failure returns a generic error and no false success dialog. |
| Headers and CSP | Security-header tests confirm nosniff, DENY framing policy, referrer policy, permissions policy and a CSP without inline scripts. |
| Contact acknowledgement integrity | The modal is flashed only after `execute()` and `commit()` complete. Validation, CSRF and database-failure tests confirm it is absent on failure. |

## Potential concerns and limitations

1. **No rate limiting:** POST endpoints have no request-frequency control. Add a trusted reverse-proxy or application-level rate limit before accepting public traffic.
2. **Local SQLite storage:** SQLite is suitable for this demo but can contend under concurrent writes and needs a retention/access-control plan before real personal data is collected.
3. **External content:** Google Fonts and the journal/studio Unsplash images remain third-party requests. Self-hosting and licence/privacy review should precede a public launch.
4. **No production delivery test:** The contact form stores the enquiry locally; it does not prove email delivery or confirm a booking.

These are implementation and deployment considerations, not confirmed vulnerabilities from the scan.
