import os
import sys
from datetime import date
from functools import wraps
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from db import get_db, init_db, close_db

load_dotenv(os.path.join(BASE_DIR, ".env"))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.secret_key = os.getenv("SECRET_KEY") or "change-this-development-secret"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
if os.getenv("VERCEL_ENV") == "production":
    app.config["SESSION_COOKIE_SECURE"] = True

app.teardown_appcontext(close_db)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.before_request
def setup_database():
    if not app.config.get("DB_READY"):
        init_db()
        app.config["DB_READY"] = True

@app.route("/")
def home():
    return redirect(url_for("dashboard") if "user_id" in session else url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter your name, a valid email and a password of at least 8 characters.", "error")
            return render_template("register.html")
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                        (name, email, generate_password_hash(password))
                    )
                    user_id = cur.fetchone()[0]
                    cur.execute("""INSERT INTO privacy_checks(user_id, title) VALUES
                        (%s, 'I use unique passwords for important accounts'),
                        (%s, 'Two-factor authentication is enabled where available'),
                        (%s, 'I reviewed app permissions recently'),
                        (%s, 'I removed accounts I no longer use')""",
                        (user_id,) * 4)
            session["user_id"] = user_id
            session["user_name"] = name
            return redirect(url_for("dashboard"))
        except psycopg2.IntegrityError:
            flash("That email may already be registered. Try logging in.", "error")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, password_hash FROM users WHERE email=%s", (email,))
                user = cur.fetchone()
        if user and check_password_hash(user[2], password):
            session["user_id"], session["user_name"] = user[0], user[1]
            return redirect(url_for("dashboard"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT COUNT(*) FROM user_accounts WHERE user_id=%s""", (session["user_id"],))
            total = cur.fetchone()[0]
            cur.execute("""SELECT COUNT(*) FROM user_accounts
                           WHERE user_id=%s AND (last_used IS NULL OR last_used < CURRENT_DATE - INTERVAL '90 days')""",
                        (session["user_id"],))
            inactive = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM privacy_checks WHERE user_id=%s AND is_done=TRUE", (session["user_id"],))
            done = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM privacy_checks WHERE user_id=%s", (session["user_id"],))
            checks = cur.fetchone()[0]
            cur.execute("""SELECT a.*, p.name AS platform, p.category
                           FROM user_accounts a JOIN platforms p ON p.id=a.platform_id
                           WHERE a.user_id=%s ORDER BY a.created_at DESC LIMIT 5""", (session["user_id"],))
            recent = cur.fetchall()
    # A simple organizational score, not a security/exposure assessment.
    score = max(0, min(100, round(100 - (inactive / total * 35 if total else 0) + (done / checks * 15 if checks else 0))))
    return render_template("dashboard.html", total=total, inactive=inactive, done=done,
                           checks=checks, score=score, recent=recent)

@app.route("/accounts")
@login_required
def accounts():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT a.*, p.name AS platform, p.category,
                                  (a.last_used IS NULL OR a.last_used < CURRENT_DATE - INTERVAL '90 days') AS needs_review
                           FROM user_accounts a JOIN platforms p ON p.id=a.platform_id
                           WHERE a.user_id=%s ORDER BY a.created_at DESC""", (session["user_id"],))
            rows = cur.fetchall()
    return render_template("accounts.html", accounts=rows, today=date.today().isoformat())

@app.route("/accounts/add", methods=["POST"])
@login_required
def add_account():
    platform = request.form.get("platform", "").strip()
    category = request.form.get("category", "Other").strip()
    username = request.form.get("username", "").strip()
    last_used = request.form.get("last_used") or None
    notes = request.form.get("notes", "").strip()
    if not platform or not username:
        flash("Platform and username/email are required.", "error")
        return redirect(url_for("accounts"))
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO platforms(name, category) VALUES (%s,%s)
                           ON CONFLICT (name) DO UPDATE SET category=EXCLUDED.category RETURNING id""",
                        (platform, category))
            platform_id = cur.fetchone()[0]
            cur.execute("""INSERT INTO user_accounts(user_id, platform_id, username, last_used, notes)
                           VALUES (%s,%s,%s,%s,%s)""",
                        (session["user_id"], platform_id, username, last_used, notes))
    flash("Account added to your registry.", "success")
    return redirect(url_for("accounts"))

@app.route("/accounts/<int:account_id>/delete", methods=["POST"])
@login_required
def delete_account(account_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM user_accounts WHERE id=%s AND user_id=%s",
                        (account_id, session["user_id"]))
    flash("Account deleted.", "success")
    return redirect(url_for("accounts"))

@app.route("/accounts/<int:account_id>/used", methods=["POST"])
@login_required
def mark_used(account_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""UPDATE user_accounts SET last_used=CURRENT_DATE
                           WHERE id=%s AND user_id=%s RETURNING id""", (account_id, session["user_id"]))
            if cur.fetchone():
                cur.execute("""INSERT INTO activity_logs(user_id, account_id, activity_type)
                               VALUES (%s,%s,'Marked as used')""", (session["user_id"], account_id))
    flash("Last-used date updated to today.", "success")
    return redirect(url_for("accounts"))

@app.route("/privacy", methods=["GET", "POST"])
@login_required
def privacy():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO privacy_checks(user_id, title) VALUES (%s,%s)",
                                (session["user_id"], title))
            flash("Checklist item added.", "success")
        return redirect(url_for("privacy"))
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, is_done FROM privacy_checks WHERE user_id=%s ORDER BY id DESC",
                        (session["user_id"],))
            items = cur.fetchall()
    return render_template("privacy.html", items=items)

@app.route("/privacy/<int:item_id>/toggle", methods=["POST"])
@login_required
def toggle_privacy(item_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""UPDATE privacy_checks SET is_done=NOT is_done
                           WHERE id=%s AND user_id=%s""", (item_id, session["user_id"]))
    return redirect(url_for("privacy"))

@app.route("/privacy/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_privacy(item_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM privacy_checks WHERE id=%s AND user_id=%s",
                        (item_id, session["user_id"]))
    return redirect(url_for("privacy"))

if __name__ == "__main__":
    app.run(debug=True)
