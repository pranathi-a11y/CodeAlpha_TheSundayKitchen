"""Flask site for The Sunday Kitchen, a sample culinary learning studio."""
import os
import re
import secrets
import sqlite3
from pathlib import Path
from flask import Flask, abort, current_app, flash, g, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from catalog import COURSES, JOURNAL, WORKSHOPS

app = Flask(__name__, instance_relative_config=True)
is_production = os.environ.get("APP_ENV", "development").strip().lower() == "production"
secret_key = os.environ.get("SECRET_KEY")
if is_production and not secret_key:
    raise RuntimeError("SECRET_KEY must be set when APP_ENV=production.")
if not secret_key:
    secret_key = secrets.token_hex(32)  # Development only; changes after process restart.
    app.logger.warning("SECRET_KEY unset: using an ephemeral development key.")
app.config.update(
    SECRET_KEY=secret_key,
    DATABASE=os.environ.get("DATABASE_PATH") or str(Path(app.instance_path) / "sunday_kitchen.sqlite3"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=is_production or os.environ.get("SESSION_COOKIE_SECURE", "0").strip() == "1",
    PERMANENT_SESSION_LIFETIME=1800,
    MAX_CONTENT_LENGTH=16 * 1024,
    WTF_CSRF_TIME_LIMIT=3600,
)
CSRFProtect(app)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def init_db():
    database = Path(current_app.config["DATABASE"])
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database, timeout=5) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL,
            enquiry_type TEXT NOT NULL CHECK(enquiry_type IN ('booking','contact')),
            workshop_slug TEXT, preferred_session TEXT, topic TEXT, message TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        connection.commit()


def get_db():
    if "db" not in g:
        database = Path(current_app.config["DATABASE"])
        database.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database, timeout=5)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.before_request
def ensure_db():
    init_db()


@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'; img-src 'self' https://images.unsplash.com data:; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self'")
    if is_production:
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
    return response


def workshop_by_slug(slug):
    return next((workshop for workshop in WORKSHOPS if workshop["slug"] == slug), None)


def person_errors(name, email, message, max_message):
    errors = {}
    if not 2 <= len(name) <= 80 or CONTROL_RE.search(name):
        errors["name"] = "Enter a name between 2 and 80 characters."
    if len(email) > 254 or not EMAIL_RE.fullmatch(email):
        errors["email"] = "Enter a valid email address."
    if len(message) > max_message or CONTROL_RE.search(message):
        errors["message"] = f"Message must be {max_message} characters or fewer."
    return errors


@app.get("/")
def home():
    return render_template("index.html", workshops=WORKSHOPS[:3], courses=COURSES[:2], journal=JOURNAL[:3])


@app.get("/workshops")
def workshops():
    return render_template("workshops.html", workshops=WORKSHOPS)


@app.get("/workshops/<slug>")
def workshop_detail(slug):
    workshop = workshop_by_slug(slug)
    if workshop is None:
        abort(404)
    return render_template("workshop_detail.html", workshop=workshop, workshops=WORKSHOPS)


@app.get("/courses")
def courses():
    return render_template("courses.html", courses=COURSES)


@app.get("/courses/<slug>")
def course_detail(slug):
    course = next((item for item in COURSES if item["slug"] == slug), None)
    if course is None:
        abort(404)
    return render_template("course_detail.html", course=course)


@app.get("/studio")
def studio():
    return render_template("studio.html", workshops=WORKSHOPS)


@app.get("/journal")
def journal():
    return render_template("journal.html", entries=JOURNAL)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    values = {"name": "", "email": "", "topic": "", "message": ""}
    errors = {}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        errors = person_errors(values["name"], values["email"], values["message"], 1500)
        if not values["message"]:
            errors["message"] = "Please tell us a little about your enquiry."
        if len(values["topic"]) > 120 or CONTROL_RE.search(values["topic"]):
            errors["topic"] = "Topic must be 120 characters or fewer."
        if errors:
            return render_template("contact.html", values=values, errors=errors), 400
        get_db().execute("INSERT INTO enquiries (name,email,enquiry_type,topic,message) VALUES (?,?,?,?,?)", (values["name"], values["email"], "contact", values["topic"] or None, values["message"]))
        get_db().commit()
        flash("Your enquiry was saved in the local demo. No email was sent.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", values=values, errors=errors)


@app.post("/enquire")
def enquire():
    values = {key: request.form.get(key, "").strip() for key in ("name", "email", "workshop", "session", "message")}
    errors = person_errors(values["name"], values["email"], values["message"], 1000)
    workshop = workshop_by_slug(values["workshop"])
    if workshop is None:
        errors["workshop"] = "Choose a workshop from the list."
    elif not any(session[0] == values["session"] for session in workshop["sessions"]):
        errors["session"] = "Choose one of the listed sample sessions."
    if errors:
        flash("Please check the details and try again.", "error")
        if workshop:
            return render_template("workshop_detail.html", workshop=workshop, workshops=WORKSHOPS, errors=errors, values=values), 400
        return render_template("workshops.html", workshops=WORKSHOPS, errors=errors, values=values), 400
    get_db().execute("INSERT INTO enquiries (name,email,enquiry_type,workshop_slug,preferred_session,message) VALUES (?,?,?,?,?,?)", (values["name"], values["email"], "booking", workshop["slug"], values["session"], values["message"]))
    get_db().commit()
    flash("Enquiry saved to the local demo database. This is not a confirmed booking; no payment was taken.", "success")
    return redirect(url_for("workshop_detail", slug=workshop["slug"]) + "#booking")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(413)
def request_too_large(_error):
    return "Request too large. Please shorten the form and try again.", 413


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
