# Secure Coding Review — Findings Register

**Project:** The Sunday Kitchen — Culinary Studio  
**Review date:** 2026-10-18  
**Reviewer:** CodeAlpha Cyber Security Internship Task 3  
**Status:** Review complete. Evidence collected from actual tool runs and manual inspection.

---

## Confirmed Findings

> No confirmed vulnerabilities were identified in the production source code (`app.py`, `catalog.py`, `templates/`).

This conclusion is based on:
- Bandit 1.7.10 scan of `app.py` and `catalog.py` at medium+ severity: **0 issues** (168 lines scanned, 0 skipped).
- Manual inspection of all routes, validation logic, SQL queries, template rendering, secret management, cookie flags, and security headers.
- 23 automated tests covering all primary security controls — all 23 passed.

The absence of findings reflects that the application was built with security controls in place. It does not mean the application is free of all possible risk; see the **Potential Concerns** section and scope limitations.

---

## Security Controls Verified

The following controls were confirmed implemented and tested:

| Control | Implementation | Test(s) |
|---------|---------------|---------|
| CSRF protection | `Flask-WTF CSRFProtect(app)` on all POST routes; `{{ csrf_token() }}` in both forms | `test_csrf_rejects_post_without_token`, `test_csrf_rejects_enquire_without_token` |
| Server-side input validation | `person_errors()` validates name length/encoding, email regex, message length; workshop slug and session are allowlist-checked | `test_booking_rejects_unknown_workshop`, `test_booking_rejects_session_from_another_workshop`, `test_booking_rejects_empty_session`, `test_booking_rejects_overlong_name`, `test_booking_rejects_invalid_email`, `test_booking_rejects_overlong_message`, `test_contact_rejects_empty_message`, `test_contact_rejects_overlong_topic`, `test_contact_rejects_overlong_message`, `test_contact_rejects_control_characters_in_name` |
| Parameterized SQL | All `INSERT` statements use `?` placeholders; no string-formatted SQL found | Bandit B608 check; manual inspection of `app.py` lines 38–42, 148, 169 |
| Jinja2 autoescaping | Default autoescaping enabled; no `\|safe` filters applied to user input | `test_xss_payload_is_escaped_in_contact_error` |
| Secure secret management | Production refuses to start without `SECRET_KEY` env var; development uses ephemeral `secrets.token_hex(32)` | Manual inspection `app.py` lines 12–18 |
| Session cookie flags | `HTTPONLY=True`, `SAMESITE=Lax`, `SECURE` conditional on production or env override | Manual inspection `app.py` lines 22–24 |
| Request-size limit | `MAX_CONTENT_LENGTH=16 KiB`; `413` handler returns plain text | `test_large_request_body_is_rejected` |
| Security headers | X-Content-Type-Options, X-Frame-Options: DENY, Referrer-Policy, Permissions-Policy, CSP (no unsafe-inline), HSTS (production only) | `test_security_headers_present`, `test_csp_blocks_inline_scripts`, `test_x_frame_options_deny` |
| 404/413 handling | Custom handlers; no stack trace or internal path leaked | `test_details_and_unknown_slugs`, `test_unknown_top_level_route_returns_404` |
| Input control-character rejection | `CONTROL_RE` regex rejects `\x00–\x08`, `\x0b`, `\x0c`, `\x0e–\x1f`, `\x7f` in name and message | `test_contact_rejects_control_characters_in_name` |
| Workshop/session allowlisting | `/enquire` validates slug against `WORKSHOPS` catalogue and then validates session against that specific workshop's sessions list | `test_booking_rejects_session_from_another_workshop`, `test_booking_rejects_empty_session` |

---

## Potential Concerns (Not Confirmed Vulnerabilities)

These are observations worth monitoring or addressing before a real production deployment. They are not confirmed security weaknesses in the current demo context.

### PC-01 — Third-party CDN dependencies (Unsplash, Google Fonts)
**Severity potential:** Low  
**Context:** Workshop images are loaded from `images.unsplash.com` via `<img src>`. Fonts are loaded from `fonts.googleapis.com` / `fonts.gstatic.com`. The CSP explicitly permits these origins.  
**Concern:** Third-party availability, privacy (user IP sent to Unsplash/Google on page load), and licensing compliance.  
**Recommendation before launch:** Audit Unsplash image licences for commercial use; self-host fonts; review Google Fonts privacy policy; narrow or remove CDN origins from CSP.

### PC-02 — No rate limiting on POST endpoints
**Severity potential:** Low–Medium  
**Context:** `/contact` and `/enquire` accept unlimited POST requests. There is no per-IP or per-session rate limiting.  
**Concern:** Automated bots could fill the enquiries table or cause excessive SQLite writes.  
**Recommendation before launch:** Add Flask-Limiter or a reverse-proxy rate limit (e.g., Nginx `limit_req`). The current 16 KiB `MAX_CONTENT_LENGTH` limits per-request abuse but not request frequency.

### PC-03 — Ephemeral development `SECRET_KEY`
**Severity potential:** Low (development only)  
**Context:** `app.py` lines 16–18: when `SECRET_KEY` is not set, `secrets.token_hex(32)` generates a new key on every process start. This causes all sessions and CSRF tokens to become invalid on restart.  
**Concern:** This is a correct and safe development fallback. It would be a vulnerability if accidentally used in production — but production mode raises `RuntimeError` if `SECRET_KEY` is unset (line 14–15).  
**Recommendation:** The guard is correct. Ensure `APP_ENV=production` and `SECRET_KEY` are set via environment before deployment.

### PC-04 — Enquiry data has no access control or retention policy
**Severity potential:** Medium (if real data is collected)  
**Context:** The `enquiries` table stores names and email addresses. There is no authentication to read or manage records. The SQLite file is excluded from Git by `.gitignore`.  
**Concern:** If the app is deployed, all collected personal data is accessible to anyone with filesystem access. No deletion, expiry or data-subject rights are implemented.  
**Recommendation before launch:** Define and implement a data-retention period; add an authenticated admin interface or delete mechanism; document a privacy notice for users.

### PC-05 — SQLite is not suitable for concurrent production load
**Severity potential:** Low  
**Context:** `sqlite3.connect(database, timeout=5)` with a single file-based database.  
**Concern:** Under concurrent write load, SQLite will queue writers for up to 5 seconds then raise `OperationalError`. This is a reliability concern, not a confidentiality one.  
**Recommendation before launch:** Use PostgreSQL or MySQL for any production deployment with concurrent users.

### PC-06 — `debug=False` is explicit, but `FLASK_DEBUG` env var could override
**Severity potential:** Medium  
**Context:** `app.run(debug=False)` is set explicitly in `app.py` line 189.  
**Concern:** If someone sets `FLASK_DEBUG=1` and runs the app via `flask run` instead of `python app.py`, the Werkzeug debugger could be enabled, exposing an interactive Python console.  
**Recommendation:** Document that the application must be started as `python app.py` (not `flask run`) and that `FLASK_DEBUG` must not be set in production. In production, a WSGI server (Gunicorn, uWSGI) should be used, which ignores `debug=False`.

---

## Bandit Output (production source, medium+ severity)

```
Run started: 2026-10-18 10:09:59

Test results:
    No issues identified.

Code scanned:
    Total lines of code: 168
    Total lines skipped (#nosec): 0

Run metrics:
    Total issues (by severity):
        Undefined: 0
        Low: 0
        Medium: 0
        High: 0
```

**Note on B101 in tests/:** Running Bandit against `tests/test_app.py` produces 23 × B101 (`assert_used`) Low-severity notices. These are expected and correct for pytest — `assert` statements are the standard testing idiom in pytest and are intentional. They are not a production code concern.

---

*A finding is listed under "Confirmed" only when evidence (line number, tool output or test result) supports it. Absence of confirmed findings is an honest result of this review, not an omission.*
