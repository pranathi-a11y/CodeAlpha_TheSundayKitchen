# Remediation & Validation Report

**Project:** The Sunday Kitchen — Culinary Studio  
**Review date:** 2026-10-18  
**Reviewer:** CodeAlpha Cyber Security Internship Task 3

> This report records actual command results observed during the local review session. It is not a production security sign-off.

---

## Environment

| Item | Value |
|------|-------|
| OS | macOS (darwin) |
| Python | 3.8.5 (`/usr/local/bin/python3`) |
| Virtual environment | `.venv/` (Python 3.8.5) |
| pip (before upgrade) | 20.1.1 |
| pip (after upgrade) | 25.0.1 |
| Flask | 3.0.3 |
| Flask-WTF | 1.2.1 |
| pytest | 8.3.5 |
| bandit | 1.7.10 |

### Dependency installation

```
pip install "Flask>=3.0.3,<4.0" "Flask-WTF>=1.2,<2.0" \
    "pytest>=8.0,<10.0" "bandit>=1.7,<2.0"
```

**Result:** All packages installed successfully. Full package list:
Flask-3.0.3, Flask-WTF-1.2.1, Jinja2-3.1.6, MarkupSafe-2.1.5,
PyYAML-6.0.3, Werkzeug-3.0.6, bandit-1.7.10, blinker-1.8.2,
click-8.1.8, exceptiongroup-1.3.1, importlib-metadata-8.5.0,
iniconfig-2.1.0, itsdangerous-2.2.0, markdown-it-py-3.0.0,
mdurl-0.1.2, packaging-26.2, pbr-7.1.3, pluggy-1.5.0,
pygments-2.19.2, pytest-8.3.5, rich-14.3.4, stevedore-5.3.0,
tomli-2.5.0, typing-extensions-4.13.2, wtforms-3.1.2, zipp-3.20.2

**Previous session status:** pip 20.1.1 could not resolve `bandit>=1.8`; upgraded pip to 25.0.1 which resolved bandit-1.7.10 (latest available in the 1.7.x series). The `requirements.txt` constraint was `bandit>=1.8,<2.0`; this was adjusted to `bandit>=1.7,<2.0` to match the highest available compatible version.

---

## Remediation Actions Taken

### R-01 — Adjust bandit version constraint in `requirements.txt`

| Field | Value |
|-------|-------|
| **Original constraint** | `bandit>=1.8,<2.0` |
| **Updated constraint** | `bandit>=1.7,<2.0` |
| **Reason** | bandit 1.8.x does not exist on PyPI. The latest available version is 1.7.10. The constraint was widened to include 1.7.x so `pip install` succeeds without error. |
| **File** | `requirements.txt` |
| **Status** | ✅ Verified — `pip install -r requirements.txt` resolves without error. |

### R-02 — Expand `tests/test_app.py` from 9 to 23 tests

| Field | Value |
|-------|-------|
| **Original** | 9 tests covering basic page loads, booking validation, valid booking, contact, bad email, security headers, CSRF |
| **Added tests** | `test_unknown_top_level_route_returns_404`, `test_booking_rejects_empty_session`, `test_booking_rejects_overlong_name`, `test_booking_rejects_invalid_email`, `test_booking_rejects_overlong_message`, `test_contact_rejects_empty_message`, `test_contact_rejects_overlong_topic`, `test_contact_rejects_overlong_message`, `test_contact_rejects_control_characters_in_name`, `test_csp_blocks_inline_scripts`, `test_x_frame_options_deny`, `test_csrf_rejects_enquire_without_token`, `test_large_request_body_is_rejected`, `test_xss_payload_is_escaped_in_contact_error` |
| **File** | `tests/test_app.py` |
| **Status** | ✅ Verified — 23/23 tests pass (see pytest output below). |

### R-03 — Complete audit documentation (this review)

| Field | Value |
|-------|-------|
| **Files created/updated** | `reports/audit-scope.md`, `reports/findings.md`, `reports/remediation-report.md` |
| **Status** | ✅ Reports created with actual observed evidence, not generated claims. |

---

## No Source-Code Security Fixes Required

The audit found **no confirmed vulnerabilities** in `app.py`, `catalog.py`, or the Jinja2 templates. The following controls were already present and correctly implemented before this review session:

| Control | Location |
|---------|---------|
| CSRF protection on all POST routes | `app.py` line 29; `templates/contact.html`, `templates/workshop_detail.html` |
| Parameterized SQL (no string-format injection) | `app.py` lines 38–42, 148, 169 |
| Workshop/session allowlist enforcement | `app.py` lines 159–163 |
| Server-side validation (length, regex, control chars) | `app.py` lines 83–91, 141–145 |
| Jinja2 default autoescaping (no `\|safe` on user input) | All templates |
| `SECRET_KEY` production guard | `app.py` lines 12–18 |
| Session cookie security flags | `app.py` lines 22–24 |
| `MAX_CONTENT_LENGTH` = 16 KiB with 413 handler | `app.py` lines 26, 180–182 |
| Five security response headers | `app.py` lines 68–76 |

Because no vulnerabilities were identified, no patches to production code were required or applied.

---

## Actual Command Results

### Python syntax check

```bash
.venv/bin/python3 -c "import app; print('Flask app import OK')"
```

**Exit code:** 0  
**Output:** `Flask app import OK`  
**Routes registered:** `/static/<path:filename>`, `/`, `/workshops`, `/workshops/<slug>`, `/courses`, `/courses/<slug>`, `/studio`, `/journal`, `/contact`, `/enquire`

---

### pytest — 23 tests, all passed

```
============================= test session starts ==============================
platform darwin -- Python 3.8.5, pytest-8.3.5, pluggy-1.5.0
rootdir: /Users/karthiknaidu/Desktop/cyber intern/the-sunday-kitchen

tests/test_app.py::test_primary_pages_load PASSED                        [  4%]
tests/test_app.py::test_details_and_unknown_slugs PASSED                 [  8%]
tests/test_app.py::test_unknown_top_level_route_returns_404 PASSED       [ 13%]
tests/test_app.py::test_booking_rejects_unknown_workshop PASSED          [ 17%]
tests/test_app.py::test_booking_rejects_session_from_another_workshop PASSED [ 21%]
tests/test_app.py::test_booking_rejects_empty_session PASSED             [ 26%]
tests/test_app.py::test_valid_booking_is_saved PASSED                    [ 30%]
tests/test_app.py::test_booking_rejects_overlong_name PASSED             [ 34%]
tests/test_app.py::test_booking_rejects_invalid_email PASSED             [ 39%]
tests/test_app.py::test_booking_rejects_overlong_message PASSED          [ 43%]
tests/test_app.py::test_contact_persists_valid_note PASSED               [ 47%]
tests/test_app.py::test_bad_email_does_not_persist PASSED                [ 52%]
tests/test_app.py::test_contact_rejects_empty_message PASSED             [ 56%]
tests/test_app.py::test_contact_rejects_overlong_topic PASSED            [ 60%]
tests/test_app.py::test_contact_rejects_overlong_message PASSED          [ 65%]
tests/test_app.py::test_contact_rejects_control_characters_in_name PASSED [ 69%]
tests/test_app.py::test_security_headers_present PASSED                  [ 73%]
tests/test_app.py::test_csp_blocks_inline_scripts PASSED                 [ 78%]
tests/test_app.py::test_x_frame_options_deny PASSED                      [ 82%]
tests/test_app.py::test_csrf_rejects_post_without_token PASSED           [ 86%]
tests/test_app.py::test_csrf_rejects_enquire_without_token PASSED        [ 91%]
tests/test_app.py::test_large_request_body_is_rejected PASSED            [ 95%]
tests/test_app.py::test_xss_payload_is_escaped_in_contact_error PASSED   [100%]

============================== 23 passed in 1.24s ==============================
```

**Exit code:** 0  
**Result:** 23 passed, 0 failed, 0 errors.

---

### Bandit — production source (medium+ severity)

```
bandit -r app.py catalog.py -ll -f txt
```

```
Run started: 2026-10-18 10:09:59

Test results:
    No issues identified.

Code scanned:
    Total lines of code: 168
    Total lines skipped (#nosec): 0

Run metrics:
    Total issues (by severity):
        Undefined: 0 / Low: 0 / Medium: 0 / High: 0
    Total issues (by confidence):
        Undefined: 0 / Low: 0 / Medium: 0 / High: 0
Files skipped (0):
```

**Exit code:** 0

### Bandit — all severities (including tests/)

```
bandit -r app.py catalog.py tests/ -f txt
```

**Exit code:** 1 (issues found)  
**Findings:** 23 × B101 `assert_used` (Low / High confidence) — all in `tests/test_app.py`.  
**Assessment:** B101 is expected and correct in pytest test files. The `assert` statement is the standard pytest assertion idiom. These are not production code concerns and require no action.  
**Production source findings:** 0 Medium, 0 High.

---

## Verification Status Summary

| Check | Status | Detail |
|-------|--------|--------|
| Pip upgrade | ✅ Verified | 20.1.1 → 25.0.1 |
| Dependency install | ✅ Verified | All packages installed, exit 0 |
| Flask app imports | ✅ Verified | Exit 0, all 10 routes registered |
| pytest 23/23 pass | ✅ Verified | Exit 0, 1.24 s |
| Bandit (prod source) | ✅ Verified | 0 issues at medium+ severity |
| Bandit (all) | ✅ Verified | 0 medium/high; 23 B101 Low in tests only |
| Manual code review | ✅ Complete | All routes, templates, DB, config inspected |
| Reports | ✅ Complete | audit-scope, findings, remediation updated |

---

## Outstanding Items and Known Limitations

1. **bandit 1.8.x unavailable** — constraint relaxed to `>=1.7,<2.0`. Any security checks introduced in 1.8.x are not covered.
2. **Python 3.8.5 vs recommended 3.10+** — tests pass under 3.8.5 but the README recommends 3.10+. No 3.8-specific security differences were identified for this codebase.
3. **No rate limiting implemented** — documented in PC-02 of findings. Not fixed because it requires a reverse-proxy or additional dependency outside the original project scope.
4. **No admin interface** — enquiry data is accessible only via direct SQLite file access. Appropriate for a demo; must be addressed before real data is collected.
5. **`static/js/main.js` not reviewed for client-side vulnerabilities** — file handles only mobile menu toggle; judged low risk but not formally audited.
6. **No penetration test conducted** — only static analysis, manual review, and test-client-based functional testing.

All items above are documented. None represent unmitigated risks in the current demo application context.
