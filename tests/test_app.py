"""
Functional and security-control tests for The Sunday Kitchen Flask application.

Tests use an isolated tmp_path SQLite database and disable CSRF for most focused
input-validation checks.  One dedicated test re-enables CSRF to confirm a POST
without a valid token is rejected (HTTP 400).

Run:
    python -m pytest tests/test_app.py -v
"""
import re
import sqlite3
import pytest
import app as project


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def app(tmp_path):
    """Provide a configured Flask test application backed by a temp database."""
    target = project.app
    target.config.update(
        TESTING=True,
        SECRET_KEY="tests-only-secret",
        DATABASE=str(tmp_path / "test.sqlite3"),
        WTF_CSRF_ENABLED=False,
        SESSION_COOKIE_SECURE=False,
    )
    with target.app_context():
        project.init_db()
    yield target


@pytest.fixture()
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def count_rows(path):
    with sqlite3.connect(path) as db:
        return db.execute("SELECT COUNT(*) FROM enquiries").fetchone()[0]


def csrf_token(response):
    """Extract the form token rendered by Flask-WTF for an integration test."""
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    assert match, "CSRF token was not rendered"
    return match.group(1).decode("utf-8")


# ---------------------------------------------------------------------------
# Basic page-load tests
# ---------------------------------------------------------------------------

def test_primary_pages_load(client):
    """All primary GET routes return HTTP 200."""
    for path in ["/", "/workshops", "/courses", "/studio", "/journal", "/contact"]:
        assert client.get(path).status_code == 200, path
    assert b"A little more" in client.get("/").data


def test_local_workshop_and_instructor_images_load(client):
    """Workshop and supplied instructor portraits are served from local static paths."""
    paths = [
        "/static/images/workshops/handmade-pasta.jpg",
        "/static/images/workshops/sourdough-sunday.jpg",
        "/static/images/workshops/little-patisserie.jpg",
        "/static/images/workshops/regional-indian-table.jpg",
        "/static/images/workshops/seasonal-market-cooking.jpg",
        "/static/images/instructors/pranathi.jpg",
        "/static/images/instructors/prakruti.jpg",
        "/static/images/instructors/amrutha-upright.jpg",
    ]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path
        assert response.mimetype == "image/jpeg"


def test_studio_has_instructors_in_requested_display_order(client):
    response = client.get("/studio")
    page = response.get_data(as_text=True)
    names = ["Pranathi Chaliseemala", "Prakruti B", "Amrutha Gowda"]
    assert all(name in page for name in names)
    assert [page.index(name) for name in names] == sorted(page.index(name) for name in names)
    assert "Meera Rao" not in page
    assert "Ananya Iyer" not in page
    assert "Kavya Nair" not in page


def test_details_and_unknown_slugs(client):
    """Known slugs return 200; unknown slugs return 404."""
    assert client.get("/workshops/handmade-pasta").status_code == 200
    assert client.get("/courses/cooking-foundations").status_code == 200
    assert client.get("/workshops/not-real").status_code == 404
    assert client.get("/courses/not-real").status_code == 404


def test_unknown_top_level_route_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404


# ---------------------------------------------------------------------------
# Booking enquiry – input validation
# ---------------------------------------------------------------------------

def test_booking_rejects_unknown_workshop(app, client):
    """Forged workshop slug is rejected; nothing persisted."""
    response = client.post(
        "/enquire",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "workshop": "fake", "session": "fake", "message": ""},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_booking_rejects_session_from_another_workshop(app, client):
    """A session slug that belongs to a different workshop is rejected."""
    response = client.post(
        "/enquire",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "workshop": "handmade-pasta",
              "session": "bread-2026-11-08",   # belongs to sourdough-sunday
              "message": ""},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_booking_rejects_empty_session(app, client):
    """Empty session value is rejected."""
    response = client.post(
        "/enquire",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "workshop": "handmade-pasta", "session": "", "message": ""},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_valid_booking_is_saved(app, client):
    """A fully valid booking enquiry is persisted with correct field values."""
    response = client.post(
        "/enquire",
        data={
            "name": "Asha Rao",
            "email": "asha@example.com",
            "workshop": "handmade-pasta",
            "session": "pasta-2026-11-07",
            "message": "Please share preparation notes.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"not a confirmed booking" in response.data
    assert count_rows(app.config["DATABASE"]) == 1
    with sqlite3.connect(app.config["DATABASE"]) as db:
        row = db.execute(
            "SELECT enquiry_type, workshop_slug, preferred_session FROM enquiries"
        ).fetchone()
    assert row == ("booking", "handmade-pasta", "pasta-2026-11-07")


def test_booking_rejects_overlong_name(app, client):
    """Name longer than 80 characters is rejected."""
    long_name = "A" * 81
    response = client.post(
        "/enquire",
        data={"name": long_name, "email": "asha@example.com",
              "workshop": "handmade-pasta", "session": "pasta-2026-11-07",
              "message": ""},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_booking_rejects_invalid_email(app, client):
    """Malformed email is rejected."""
    response = client.post(
        "/enquire",
        data={"name": "Asha Rao", "email": "not-an-email",
              "workshop": "handmade-pasta", "session": "pasta-2026-11-07",
              "message": ""},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_booking_rejects_overlong_message(app, client):
    """Message exceeding 1000 characters is rejected."""
    long_msg = "x" * 1001
    response = client.post(
        "/enquire",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "workshop": "handmade-pasta", "session": "pasta-2026-11-07",
              "message": long_msg},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


# ---------------------------------------------------------------------------
# Contact form – input validation
# ---------------------------------------------------------------------------

def test_contact_persists_valid_note(app, client):
    """A valid contact note is persisted."""
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "topic": "Course enquiry",
              "message": "Could you share the syllabus?"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Sent!" in response.data
    assert b"Thank you for reaching out. Your message has been received." in response.data
    assert b"data-contact-success" in response.data
    assert count_rows(app.config["DATABASE"]) == 1


def test_contact_success_modal_follows_a_valid_csrf_protected_submission(app, client):
    """The success modal is rendered only after a valid, protected save succeeds."""
    app.config["WTF_CSRF_ENABLED"] = True
    token = csrf_token(client.get("/contact"))
    response = client.post(
        "/contact",
        data={
            "csrf_token": token,
            "name": "Asha Rao",
            "email": "asha@example.com",
            "topic": "Course enquiry",
            "message": "Could you share the syllabus?",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"data-contact-success" in response.data
    assert count_rows(app.config["DATABASE"]) == 1


def test_bad_email_does_not_persist(app, client):
    """An invalid email on the contact form is rejected; nothing persisted."""
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "not-email",
              "topic": "", "message": "Hello"},
    )
    assert response.status_code == 400
    assert b"data-contact-success" not in response.data
    assert count_rows(app.config["DATABASE"]) == 0


def test_contact_rejects_empty_message(app, client):
    """An empty message body is rejected."""
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "topic": "", "message": ""},
    )
    assert response.status_code == 400
    assert b"data-contact-success" not in response.data
    assert count_rows(app.config["DATABASE"]) == 0


def test_contact_rejects_overlong_topic(app, client):
    """A topic string exceeding 120 characters is rejected."""
    long_topic = "T" * 121
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "topic": long_topic, "message": "Hello there"},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_contact_rejects_overlong_message(app, client):
    """A message exceeding 1500 characters is rejected."""
    long_msg = "x" * 1501
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "topic": "", "message": long_msg},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_contact_rejects_control_characters_in_name(app, client):
    """Control characters embedded in name are rejected."""
    response = client.post(
        "/contact",
        data={"name": "Asha\x00Rao", "email": "asha@example.com",
              "topic": "", "message": "Hello"},
    )
    assert response.status_code == 400
    assert count_rows(app.config["DATABASE"]) == 0


def test_contact_database_failure_is_controlled_and_never_shows_success(app, client, monkeypatch):
    """A SQLite write failure returns a generic error without a false acknowledgement."""
    class FailingDatabase:
        def execute(self, *_args, **_kwargs):
            raise sqlite3.OperationalError("database is locked")

        def rollback(self):
            return None

    monkeypatch.setattr(project, "get_db", lambda: FailingDatabase())
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "asha@example.com", "topic": "", "message": "Hello"},
    )
    assert response.status_code == 500
    assert b"We couldn&#39;t save your message" in response.data
    assert b"data-contact-success" not in response.data
    assert count_rows(app.config["DATABASE"]) == 0


# ---------------------------------------------------------------------------
# Security header checks
# ---------------------------------------------------------------------------

def test_security_headers_present(client):
    """Key security headers are present on a standard GET response."""
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in response.headers


def test_csp_blocks_inline_scripts(client):
    """CSP does not include unsafe-inline in script-src."""
    csp = client.get("/").headers.get("Content-Security-Policy", "")
    assert "unsafe-inline" not in csp


def test_x_frame_options_deny(client):
    """X-Frame-Options must be DENY to prevent clickjacking."""
    response = client.get("/")
    assert response.headers["X-Frame-Options"] == "DENY"


# ---------------------------------------------------------------------------
# CSRF protection
# ---------------------------------------------------------------------------

def test_csrf_rejects_post_without_token(app, client):
    """POSTing without a CSRF token is rejected with HTTP 400."""
    app.config["WTF_CSRF_ENABLED"] = True
    response = client.post(
        "/contact",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "topic": "", "message": "Hello"},
    )
    assert response.status_code == 400
    assert b"data-contact-success" not in response.data


def test_csrf_rejects_enquire_without_token(app, client):
    """Booking POST without a CSRF token is also rejected."""
    app.config["WTF_CSRF_ENABLED"] = True
    response = client.post(
        "/enquire",
        data={"name": "Asha Rao", "email": "asha@example.com",
              "workshop": "handmade-pasta", "session": "pasta-2026-11-07",
              "message": ""},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Request-size limit (MAX_CONTENT_LENGTH = 16 KiB)
# ---------------------------------------------------------------------------

def test_large_request_body_is_rejected(app, client):
    """A request body exceeding MAX_CONTENT_LENGTH returns HTTP 413."""
    app.config["WTF_CSRF_ENABLED"] = False
    big_payload = "x" * (17 * 1024)
    response = client.post(
        "/contact",
        data={"name": "Asha", "email": "a@b.com", "topic": "", "message": big_payload},
        content_type="application/x-www-form-urlencoded",
    )
    assert response.status_code == 413


# ---------------------------------------------------------------------------
# XSS – verify Jinja autoescaping on reflected values
# ---------------------------------------------------------------------------

def test_xss_payload_is_escaped_in_contact_error(app, client):
    """A script tag submitted to the contact form is HTML-escaped in the error response."""
    payload = "<script>alert(1)</script>"
    response = client.post(
        "/contact",
        data={"name": payload, "email": "bad", "topic": "", "message": ""},
    )
    assert response.status_code == 400
    # The raw script tag must not appear verbatim; it must be escaped.
    assert b"<script>alert(1)</script>" not in response.data
    assert b"&lt;script&gt;" in response.data
