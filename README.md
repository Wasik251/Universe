# UniVerse

**Movies. Games. Academics. Friends. All in one universe.**

UniVerse is an all-in-one student platform built with Flask. Share short posts, review movies and games, find teammates for games, study with the Academic Hub, and chat live with fellow students.

## Features

- **Welcome page** — landing page with Log In / Sign Up
- **Authentication** — sign up with name, username, email, **date of birth** (system checks 10+ eligibility), password; log in with username or email; **stay logged in** (permanent sessions, remember me)
- **Feed** — short posts with likes, **emoji reactions**, share links, live timestamps; delete your own posts
- **Chat** — live community chat with auto-refresh and colorful bubbles
- **Movies** — browse, search, review, and watchlist
- **Games** — browse, search, review, game library with statuses, LFG (Looking For Group)
- **Academic Hub** — departments, courses, study notes, past questions, MCQs, discussion threads
- **Profiles** — bios, follow system, admin badges, colorful gradient avatars
- **Users directory** — searchable list of all members
- **Manage Center** — admin-only (password `313121`): add/delete movies & games, **delete users**, moderate posts
- **Database Manager** — admin-only: view every table & row count, **download full JSON backup**, reset the database
- **Colorful dynamic UI** — animated aurora background, gradient borders, rainbow buttons, sound effects on every click
- **Logout** — returns you to the home/welcome page

## Run locally

```bash
cd universe_app
pip install -r requirements.txt
python app.py
```

Open http://localhost:8080

### Demo accounts
| Username | Password | Role |
|----------|----------|------|
| `alice` | `pass` | Member |
| `bob` | `pass` | Member |
| `admin` | `313121` | Admin |

## Deploy on Vercel

The repo includes `vercel.json` and `api/index.py` for serverless deployment.

1. Import the repo at https://vercel.com
2. Add env var `SECRET_KEY` (any random string)
3. **Required for accounts to persist and stay logged in** — add a persistent database:

   - Create a free Postgres database at https://neon.tech (or https://supabase.com)
   - Copy the connection string and add it as env var `DATABASE_URL` in Vercel
   - This fixes both "asked to log in again" and "signups disappear" — Vercel's `/tmp` SQLite is wiped on cold starts and differs per server instance, so accounts vanish without a shared database

4. Deploy

> Note: on the free tier without `DATABASE_URL`, data resets on cold starts.
> You can download a full JSON backup anytime from **Manage → Database → Export Backup**.
