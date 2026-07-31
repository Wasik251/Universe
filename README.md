# UniVerse

**Movies. Games. Academics. Friends. All in one universe.**

UniVerse is an all-in-one student platform built with Flask. Share short posts, review movies and games, find teammates for games, study with the Academic Hub, and chat live with fellow students.

## Features

- **Welcome page** — landing page with Log In / Sign Up
- **Authentication** — sign up with name, username, email, age, password (age 10+ required); log in with username or email
- **Feed** — short posts with likes; delete your own posts
- **Chat** — live community chat with auto-refresh
- **Movies** — browse, search, review, and watchlist
- **Games** — browse, search, review, game library with statuses, LFG (Looking For Group)
- **Academic Hub** — departments, courses, study notes, past questions, MCQs, discussion threads
- **Profiles** — bios, follow system, admin badges
- **Users directory** — searchable list of all members
- **Manage Center** — admin-only (password `313121`): add/delete movies & games, view users, moderate posts
- **Sound effects** — "bing bong" on every button click
- **Dynamic UI** — gradients, glowing buttons, animated elements

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
3. Deploy

> Note: the free tier uses SQLite in `/tmp`, so data resets on cold starts.
