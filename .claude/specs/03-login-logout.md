# Spec: Login and Logout

## Overview
This feature makes `/login` and `/logout` functional. `POST /login` validates submitted credentials against the `users` table, checks the password hash, and on success starts a session by storing the user's id in Flask's session cookie, then sends the user to the landing page with a "Welcome back" greeting. `GET /logout` clears that session and sends the user back to the landing page too. This is Step 3 on the Spendly roadmap, directly after registration — it's the first place the app reads back the credentials created in Step 2 and the first time a session cookie (promised in `templates/privacy.html`, section 5) is actually set.

## Depends on
- Step 01 (Database setup) — `database/db.py` with `get_db()`, `users` table with `password_hash`. Already implemented.
- Step 02 (Registration) — `POST /register` creates the hashed-password rows this step authenticates against. Already implemented.

## Routes
- `GET /login` — render the sign-in form; redirects to `/` if already logged in — public
- `POST /login` — validate credentials, start session on success, redirect to `/` — public
- `GET /logout` — clear the session, redirect to `/` — logged-in (safe no-op if no session exists)
- `GET /register` — render the registration form; redirects to `/` if already logged in — public (behavior addition to Step 02's route, since Step 02 predates sessions existing)

## Database changes
No database changes. `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already has everything login needs.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — pre-fill the submitted `email` on error (same pattern as `register.html`'s `value="{{ email or '' }}"`), so the user doesn't have to retype it
  - `templates/base.html` — nav links become session-aware: when `session.user_id` is set, show "Profile" (linking to `/profile`) and "Logout" (linking to `/logout`) instead of "Sign in" / "Get started". Flask injects `session` into the Jinja context automatically, so no view changes are needed to read it in the template.
  - `templates/landing.html` — the hero badge becomes session-aware: when `session.user_id` is set, show "Welcome back, {{ session.user_name }}!" using the existing `.hero-v2-badge` styling instead of the "Free to use · No credit card needed" copy

## Files to change
- `app.py`:
  - Import `session` from `flask` and `check_password_hash` from `werkzeug.security`
  - Set `app.secret_key` (hardcoded dev constant — no config/env mechanism exists yet in this project; revisit when one is added)
  - Implement `POST` handling on `/login`: look up user by email, verify password with `check_password_hash`, set `session["user_id"]` and `session["user_name"]` on success, redirect to `/`; on failure re-render `login.html` with an error and the submitted email
  - Implement `/logout`: clear the session (`session.clear()`) and redirect to `/`
  - Guard both `login()` and `register()`: if `session.get("user_id")` is set, redirect to `/` immediately (before checking `request.method`), so an already-logged-in user can't reach either form
- `templates/login.html` — pre-fill email on error
- `templates/base.html` — session-aware nav links
- `templates/landing.html` — session-aware "Welcome back" hero badge

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — this step only ever compares with `check_password_hash`, never re-hashes or stores plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate on the server even though the form has HTML5 `required`/`type` attributes
- Use one generic error message ("Invalid email or password") for both "no such user" and "wrong password" cases — don't reveal whether an email is registered
- `/profile` and the other placeholder routes (`/expenses/...`) are NOT gated behind a login check in this step — that stays out of scope; this step only covers setting and clearing the session
- Keep the existing separation in `app.py` between implemented routes and the placeholder-routes block; `/logout` moves from the placeholder block to the implemented-routes block since it's now real

## Definition of done
- [ ] Submitting `/login` with the seeded demo user (`demo@spendly.com` / `demo123`) redirects to `/` and sets a session cookie
- [ ] After that redirect, the landing page hero badge reads "Welcome back, Demo User!" instead of "Free to use · No credit card needed"
- [ ] Submitting `/login` with a registered email but wrong password re-renders `login.html` with a generic error and does not set a session cookie
- [ ] Submitting `/login` with an email that isn't registered re-renders `login.html` with the same generic error
- [ ] After logging in, the navbar shows "Profile" and "Logout" instead of "Sign in" / "Get started" on every page
- [ ] Visiting `/logout` after logging in clears the session, redirects to `/`, the hero badge reverts to "Free to use · No credit card needed", and the navbar reverts to "Sign in" / "Get started"
- [ ] Visiting `/logout` with no active session does not error and redirects to `/`
- [ ] `GET /login` still renders the empty form as before
- [ ] While logged in, visiting `/login` or `/register` redirects to `/` instead of rendering the form
- [ ] While logged out, `/login` and `/register` render normally
