"""EivaBot — a simple Telegram userbot based on Telethon."""

[![GitHub license](https://img.shields.io/github/license/TeamEiva/Eivabot?&style=flat-square&logo=github)](https://github.com/TeamEiva/Eivabot/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/TeamEiva/Eivabot?&style=flat-square&logo=github)](https://github.com/TeamEiva/Eivabot/issues)

## What is EivaBot?

EivaBot is a modular Telegram **userbot** (runs on your own user account via a
Telethon `StringSession`) built for fun commands and easier group management.

## Requirements

* Python **3.9 – 3.12** (3.11 recommended)
* A Telegram account and [API credentials](https://my.telegram.org) (`APP_ID`, `API_HASH`)
* A generated session string (see below)

## Local installation

```bash
git clone https://github.com/TeamEiva/Eivabot.git
cd Eivabot

python -m venv .venv
# Windows PowerShell:
. .venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 1. Get your Telegram API credentials

1. Visit <https://my.telegram.org>, log in, open **API Development Tools**
2. Create an application and note the `APP_ID` (integer) and `API_HASH`.

### 2. Generate your session string

```bash
python stringsetup.py
```

Enter your `APP_ID` / `API_HASH`, log in with the OTP code Telegram sends you,
and the session string will be printed **and** sent to your Telegram *Saved
Messages*. Treat this string like a password — anyone holding it can control
your account.

### 3. Configure environment variables

```bash
cp .env.example .env   # then edit .env with your real values
```

| Variable | Required | Description |
|---|---|---|
| `APP_ID` | ✅ | from my.telegram.org |
| `API_HASH` | ✅ | from my.telegram.org |
| `EivaBOT_SESSION` | ✅ | Telethon StringSession from step 2 |
| `LOGGER_ID` | – | private log channel id (starts with `-100`) |
| `BOT_TOKEN` / `BOT_USERNAME` | – | helper bot from @BotFather |
| `HANDLER` | – | command prefix (default `.`) |
| `PM_PERMIT` | – | `ENABLE` / `DISABLE` |
| `SUDO_USERS` | – | space-separated user ids with extra access |
| `HEROKU_API_KEY` / `HEROKU_APP_NAME` | – | needed only for the Heroku updater |

### 4. Run

```bash
python -m Eivabot
```

Note: the full plugin suite lives in
[TeamEiva/Eiva-Userbot](https://github.com/TeamEiva/Eiva-Userbot). On Heroku /
Docker the `Eivabot` launcher script downloads that package automatically and
runs `python3 -m Eivabot` from inside it, unlocking all plugins. Running from
this checkout directly starts the core bot (client + config validation) without
the optional plugins.

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TeamEiva/EivaBot)

Or with `heroku.yml` (container stack): push the repo and set the stack to
`container`:

```bash
heroku stack:set container -a <app-name>
git push heroku main
```

Set the environment variables listed above on the Heroku app (`heroku config:set ...`).

## Deploy with Docker

```bash
docker build -t eivabot .
docker run -d --name eivabot \
  -e APP_ID=12345 \
  -e API_HASH=... \
  -e EivaBOT_SESSION=... \
  eivabot
```

## Deploy to Railway

Fork this repository, then in [Railway](https://railway.app) create a new
project → *Deploy from GitHub repo*. Set the same environment variables in the
Railway dashboard (Railway auto-detects the `Procfile`/`Dockerfile`). Railway's
modern runtime supports Python 3.11 natively; no template repo is required
anymore.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Missing required environment variables: ...` | one or more of `APP_ID`, `API_HASH`, `EivaBOT_SESSION` is unset — copy `.env.example` to `.env` and fill it in |
| `APP_ID must be an integer` | copy the numeric App ID from my.telegram.org, not the App title |
| `AuthKeyDuplicatedError` on start | the session string was regenerated/used elsewhere — generate a fresh one with `stringsetup.py` |
| `HTTP 401 / AUTH_KEY_UNREGISTERED` | the session was revoked (logout or password change) — regenerate |
| pip build failures on old Python | use Python ≥ 3.9 (3.11 recommended) |
| `FloodWait` errors | you are hitting rate limits — wait the reported number of seconds; do not loop-send messages |

## Security recommendations

* **Never** commit `.env`, session strings, or `*.session` files (both are in `.gitignore`).
* Use a dedicated Telegram account for the userbot if possible.
* Regenerate the session string immediately if it leaks — it grants full account access.
* Keep dependencies updated; run `pip list --outdated` occasionally.

## Breaking changes in this modernized version

* Python **3.11** is now the target runtime (`runtime.txt` updated; 3.9.2 removed).
* `requirements.txt` was rewritten with pinned, installable versions. Dozens of
  unmaintained/dead packages (e.g. `cfscrape`, `coffeehouse`, `opencv-python--headless`
  (typo'd spec), `googletrans==4.0.0-rc1`, `sqlalchemy==1.3.23`) were removed
  because they no longer install on modern Python or their plugins no longer load.
* Deploy buttons now reflect the main branch; Railway deploys from a fork directly.
* The launcher (`Eivabot`) now installs full requirements instead of a diff-only
  update, uses `set -euo pipefail`, and `exec`s the bot for proper signal handling.
* `app.json` no longer requires a Mongo addon / Heroku API key to deploy.

## Disclaimer

You are forewarned: your Telegram account may get banned. EivaBot and its
maintainers are not responsible for your account. This bot is intended for fun
commands and helpful group management — do not spam.

## Credits

* [LonamiWebs/Telethon](https://github.com/LonamiWebs/Telethon)
* All [contributors of Eivabot](https://github.com/TeamEiva/Eivabot/graphs/contributors)
* [Dark Cobra](https://github.com/DARK-COBRA/DARKCOBRA)

Licensed under the GNU GPL-3.0 (see [LICENSE](LICENSE)).
