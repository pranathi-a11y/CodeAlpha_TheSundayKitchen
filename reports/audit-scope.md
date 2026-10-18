# Secure Coding Review — Audit Scope

**Project:** The Sunday Kitchen — Culinary Studio  
**Review date:** 2026-10-18  
**Reviewer:** CodeAlpha Cyber Security Internship Task 3  
**Language / framework:** Python 3.8.5 · Flask 3.0.3 · Flask-WTF 1.2.1  
**Database:** SQLite (local file via `sqlite3` stdlib)  
**Template engine:** Jinja2 3.1.6  
**Static assets:** CSS (`static/css/styles.css`), JavaScript (`static/js/main.js`)

---

## Files reviewed

| File | Purpose |
|------|---------|
| `app.py` (190 lines) | Flask application factory, routes, validation, DB helpers |
| `catalog.py` (20 lines) | Static catalogue data (workshops, courses, journal) |
| `templates/base.html` | Site-wide HTML shell, nav, flash messages |
| `templates/contact.html` | Contact/enquiry form with CSRF token |
| `templates/workshop_detail.html` | Workshop page with booking form |
| `templates/workshops.html` | Workshop listing |
| `templates/courses.html` | Course listing |
| `templates/course_detail.html` | Course detail |
| `templates/studio.html` | Studio page |
| `templates/journal.html` | Journal listing |
| `templates/404.html` | Custom 404 page |
| `tests/test_app.py` | Automated functional and security tests |
| `requirements.txt` | Pinned dependency bounds |
| `.gitignore` | Repo exclusions (`.env`, `.venv`, `instance/*.sqlite3`) |
| `.env.example` | Example environment variables |
| `README.md` | Local run and audit instructions |

---

## Review methods

| Method | Tools / commands |
|--------|----------------|
| Static analysis | `bandit -r app.py catalog.py -ll -f txt` (medium+ severity) |
| Full low-severity scan | `bandit -r app.py catalog.py tests/ -f txt` |
| Automated functional tests | `pytest tests/test_app.py -v` |
| Manual inspection | Line-by-line review of routes, validation logic, SQL, templates, config |

### Exact commands run

```bash
# Upgrade pip (was 20.1.1)
.venv/bin/python3 -m pip install --upgrade pip

# Install all dependencies
.venv/bin/pip install "Flask>=3.0.3,<4.0" "Flask-WTF>=1.2,<2.0" \
    "pytest>=8.0,<10.0" "bandit>=1.7,<2.0"

# Run tests
.venv/bin/python3 -m pytest tests/test_app.py -v

# Run Bandit (production source, medium+ severity)
.venv/bin/python3 -m bandit -r app.py catalog.py -ll -f txt

# Full Bandit scan (all severities, includes tests/)
.venv/bin/python3 -m bandit -r app.py catalog.py tests/ -f txt
```

---

## In scope

- All Flask routes and 404/413 error handlers.
- Contact (`/contact`) and booking (`/enquire`) POST endpoints: input validation, CSRF, DB persistence.
- SQLite schema constraints and parameterized queries.
- Session cookie configuration (`HTTPONLY`, `SAMESITE`, `SECURE` flags).
- Secret key management and environment-variable handling.
- `MAX_CONTENT_LENGTH` request-size enforcement.
- HTTP response security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Content-Security-Policy`, `Strict-Transport-Security`).
- Jinja2 autoescaping of user-supplied values.
- Python import security (`secrets`, `re`, `os`, `sqlite3` from stdlib).

---

## Out of scope

- Production hosting, TLS termination, reverse-proxy configuration, load balancing, uptime monitoring, backups.
- Unsplash image CDN and Google Fonts CDN: third-party availability, privacy policy, licensing compliance.
- Verification of real business details, actual class availability, email delivery, payment processing or booking confirmation (none implemented).
- Penetration testing against a deployed service.
- Front-end JavaScript (`static/js/main.js`) dynamic behaviour beyond template inspection.
- Dependency supply-chain analysis (sub-dependencies of Flask, WTForms, Werkzeug, etc.).
- Authentication or administration interfaces (none exist).

---

## Limitations

- Testing was conducted locally against `Python 3.8.5`. The README recommends Python 3.10+; behaviour differences in cryptographic primitives or standard-library modules between versions were not evaluated.
- Bandit 1.7.10 was the latest version available on PyPI compatible with this environment. Version 1.8+ could not be installed.
- No network-accessible deployment was available; all tests use Flask's built-in test client against a temporary SQLite database.
- The `static/js/main.js` file was not reviewed for client-side vulnerabilities (e.g., DOM-based XSS, prototype pollution) — it handles only mobile menu toggle behaviour.
- Ordinary form tests disable CSRF (`WTF_CSRF_ENABLED=False`) to focus on input-validation logic. Two dedicated tests re-enable CSRF and confirm POST requests without a valid token are rejected. Passing tests or static analysis does not prove the application secure.
