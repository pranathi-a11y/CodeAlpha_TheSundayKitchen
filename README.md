# CodeAlpha Cyber Security Internship — Task 3: Secure Coding Review

**Project audited:** The Sunday Kitchen — Culinary Studio  
**Language:** Python  
**Web framework:** Flask  
**Review date:** 18 October 2026

This repository contains the application and review evidence prepared for CodeAlpha's **Task 3: Secure Coding Review**. The task asks the intern to select a programming language and application, review the code for security vulnerabilities using static-analysis tools and/or manual inspection, recommend secure-coding practices, and document findings with remediation steps.

## Project overview

The Sunday Kitchen is a demonstration website for a fictional culinary learning studio. It includes workshop and course pages, studio and journal pages, and contact and booking-enquiry forms. It is not a live restaurant, booking, payment, or email service. Content, fees, schedules, and contact details are illustrative.

## Secure coding review

The review focused on the Flask application, templates, request validation, database access, session configuration, secret handling, and HTTP response security headers.

### Methods and evidence

- **Manual source review** of routes, form handling, validation, SQL statements, templates, and configuration.
- **Bandit static analysis** against the production Python source (`app.py` and `catalog.py`) at medium-and-higher severity.
- **Automated tests** for functional behaviour and security controls, including CSRF rejection, input validation, request-size handling, response headers, unknown routes, and output escaping.
- **Written audit records** documenting scope, findings, remediation and test results.

### Results

The recorded review found **no confirmed vulnerabilities** in the reviewed production Python source and Jinja templates. The Bandit scan of `app.py` and `catalog.py` reported no medium- or high-severity issues, and the project's test report records **23 passing tests**.

That result is not a guarantee that the application is vulnerability-free or ready for production. The reports document potential concerns and limitations, including no rate limiting on form submissions, third-party CDN privacy/licensing considerations, and the fact that this was a local review rather than a deployed penetration test.

### Security controls reviewed

- CSRF protection on form POST requests
- Server-side input validation and workshop/session allowlists
- Parameterized SQLite statements
- Jinja autoescaping for rendered user input
- Production guard requiring an explicitly configured secret key
- Session cookie flags
- Request body size limit and controlled 404/413 responses
- HTTP security headers, including Content Security Policy
- Persistence and validation behaviour covered by automated tests

See [`reports/audit-scope.md`](reports/audit-scope.md), [`reports/findings.md`](reports/findings.md), [`reports/remediation-report.md`](reports/remediation-report.md), and [`reports/bandit-output.txt`](reports/bandit-output.txt) for the supporting evidence.

## Run locally

Python 3.10 or later is recommended. The review report records execution in a Python 3.8.5 environment.

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Set a development secret and start the application:

   ```bash
   export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
   export APP_ENV=development
   python app.py
   ```

4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

The SQLite database is generated locally and should not be committed. For production, configure a strong secret through the environment, HTTPS, and the appropriate secure cookie settings.

## Run the checks

Run the test suite:

```bash
python -m pytest -q
```

Run Bandit against the production Python source:

```bash
python -m bandit -r app.py catalog.py -ll -f txt
```

A passing test suite or clean static-analysis result alone does not prove that software is secure. Review the documented scope and limitations alongside the results.

## Repository structure

- `app.py`, `catalog.py` — Flask application and catalogue data
- `templates/` — Jinja templates for pages and forms
- `static/` — CSS and JavaScript assets
- `tests/test_app.py` — functional and security-oriented tests
- `reports/audit-scope.md` — scope, methods, exclusions, and limitations
- `reports/findings.md` — confirmed findings and potential concerns
- `reports/remediation-report.md` — remediation and validation evidence
- `reports/bandit-output.txt` — saved static-analysis output
- `requirements.txt`, `.env.example`, `.gitignore` — dependencies and local configuration guidance

## Before production use

Review and address the documented potential concerns; add appropriate rate limiting; confirm data-retention and privacy practices; review third-party asset licensing; and arrange deployment hardening, monitoring, and further security testing. The current demonstration does not implement user authentication, an admin interface, real email delivery, payments, or confirmed bookings.

## Task reference

This project addresses **CodeAlpha Cyber Security Internship Task 3 — Secure Coding Review**. The internship instructions request that completed source code be uploaded to a GitHub repository named `CodeAlpha_ProjectName`, a project explanation video be posted on LinkedIn with the repository link, and the completed task be submitted through the provided submission form. Follow the official instructions and deadline supplied for your batch.
