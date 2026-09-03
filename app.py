import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        return render_template(
            "register.html",
            error="Please fill in all fields.",
            name=name,
            email=email,
        )

    if "@" not in email:
        return render_template(
            "register.html",
            error="Please enter a valid email address.",
            name=name,
            email=email,
        )

    if len(password) < 8:
        return render_template(
            "register.html",
            error="Password must be at least 8 characters.",
            name=name,
            email=email,
        )

    if password != confirm_password:
        return render_template(
            "register.html",
            error="Passwords do not match.",
            name=name,
            email=email,
        )

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing is not None:
            return render_template(
                "register.html",
                error="An account with this email already exists.",
                name=name,
                email=email,
            )

        password_hash = generate_password_hash(password)
        try:
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="An account with this email already exists.",
                name=name,
                email=email,
            )
    finally:
        conn.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = "Invalid email or password."

    if not email or not password:
        return render_template("login.html", error=error, email=email)

    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error=error, email=email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Ayesha Khan",
        "email": "ayesha.khan@example.com",
        "initials": "AK",
        "member_since": "March 2025",
    }

    stats = [
        {"label": "Total spent", "value": "PKR 48,320"},
        {"label": "Transactions", "value": "27"},
        {"label": "Top category", "value": "Bills"},
    ]

    transactions = [
        {"date": "2026-08-29", "description": "Electricity bill", "slug": "bills", "label": "Bills", "amount": "4,500"},
        {"date": "2026-08-27", "description": "Grocery run at Al-Fatah", "slug": "food", "label": "Food", "amount": "1,850"},
        {"date": "2026-08-24", "description": "Careem ride to office", "slug": "transport", "label": "Transport", "amount": "420"},
        {"date": "2026-08-20", "description": "Dentist appointment", "slug": "health", "label": "Health", "amount": "3,000"},
        {"date": "2026-08-18", "description": "Movie night — Cinepax", "slug": "entertainment", "label": "Entertainment", "amount": "1,200"},
        {"date": "2026-08-15", "description": "New winter jacket", "slug": "shopping", "label": "Shopping", "amount": "6,750"},
    ]

    categories = [
        {"label": "Bills", "slug": "bills", "amount": "PKR 12,400", "width_class": "cat-w-100"},
        {"label": "Shopping", "slug": "shopping", "amount": "PKR 9,750", "width_class": "cat-w-80"},
        {"label": "Food", "slug": "food", "amount": "PKR 8,200", "width_class": "cat-w-70"},
        {"label": "Health", "slug": "health", "amount": "PKR 6,100", "width_class": "cat-w-50"},
        {"label": "Entertainment", "slug": "entertainment", "amount": "PKR 4,900", "width_class": "cat-w-40"},
        {"label": "Transport", "slug": "transport", "amount": "PKR 4,270", "width_class": "cat-w-30"},
        {"label": "Other", "slug": "other", "amount": "PKR 2,700", "width_class": "cat-w-20"},
    ]

    return render_template(
        "profile.html", user=user, stats=stats,
        transactions=transactions, categories=categories,
    )


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
