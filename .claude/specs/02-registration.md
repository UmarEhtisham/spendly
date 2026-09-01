# Spec: Registration

## Overview
This feature makes the `/register` route functional: it accepts the existing `register.html` form submission, validates input, creates a new user in the `users` table with a hashed password, and redirects to `/login` so the user can sign in with their new credentials. It's the first write path in the app and the first place user-supplied input reaches the database, so validation and parameterised queries matter here. This is Step 2 on the Spendly roadmap, immediately after the database layer.

## Depends on
- Step 01 (Database setup) — `database/db.py` with `get_db()`, `init_db()`, `users` table. Already implemented.

## Routes
- `GET /register` — render the registration form — public (already implemented, unchanged)
- `POST /register` — validate submitted form data, create the user, redirect to `/login` — public

## Database changes
No database changes. `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already exists in `database/db.py` and covers everything registration needs.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — add a `confirm_password` field alongside `password`, and re-render the form with the submitted `name`/`email` pre-filled and `{{ error }}` populated when validation or a duplicate email fails, so the user doesn't have to retype everything

## Files to change
- `app.py` — implement `POST` handling on `/register` (validation, duplicate-email check, password hashing, insert, redirect to `/login`)

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate on the server even though the form has HTML5 `required`/`type` attributes — never trust client-side validation alone
- The form has a `confirm_password` field; reject the submission with an error if it doesn't match `password`
- Check for an existing email via a `SELECT` before inserting, and also handle the `sqlite3.IntegrityError` from the `UNIQUE` constraint as a fallback, since a race between the check and insert is possible
- Registration does not auto-login — on success, redirect to `/login` and let the user sign in with their new credentials there. No `flask.session` usage in this step; the "single session cookie" promised in `templates/privacy.html` is established by the future `/login` implementation, not here
- Do not implement `/login` (POST handling), `/logout`, or `/profile` beyond what already exists — those stay out of scope for this step
- Keep the existing separation in `app.py` between implemented routes and the placeholder-routes block

## Definition of done
- [ ] Submitting the register form with valid, unused name/email/password creates a row in `users` with a hashed (not plaintext) password
- [ ] After successful registration, the browser is redirected to `/login` (no session cookie is set)
- [ ] Submitting with an email that already exists re-renders `register.html` with an error message and does not create a duplicate row
- [ ] Submitting with a missing/empty field re-renders `register.html` with an error message and does not hit the database
- [ ] Submitting with `password` and `confirm_password` that don't match re-renders `register.html` with an error message and does not hit the database
- [ ] Restarting the app and re-registering the same demo email (`demo@spendly.com`) still correctly rejects as a duplicate
- [ ] `GET /register` still renders the empty form as before
