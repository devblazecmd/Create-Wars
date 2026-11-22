---
tags: [design, mc-version/1.21.1, loader/neoforge]
status: active
---

# Server Deployment

## Decision (owner, 2026-11-22)
First multiplayer test with friends: **rented host**, pack distributed from a **public GitHub repo** so the server and every
player auto-update with packwiz on each start/launch.

## Mechanics
- Pack URL: `https://raw.githubusercontent.com/devblazecmd/Create-Wars/main/pack/pack.toml` (needs the repo public).
- `server/` in the repo: `start.sh`/`start.bat` (downloads packwiz-installer-bootstrap v0.0.3 if missing, runs it with
  `-g -s server`, then NeoForge's `run.sh nogui`), `server.properties.recommended`, `user_jvm_args.txt` (10 GB),
  `README.md` (host steps + Prism steps for players).
- `-s server` skips client-only mods (Sodium, Iris, Iris-Flywheel compat, ImmediatelyFast, EntityCulling,
  BadOptimizations, Create Better FPS) and installs server-only ones (Alternate Current).
- Key server settings: `allow-flight=true` (Aeronautics/Sable craft move players; without it they get kicked),
  `max-tick-time=-1` (heavy Create/Sable ticks can trip the watchdog), `pvp=true`, whitelist on, `spawn-protection=0`.
- Pushing to `main` updates everyone on their next restart/launch. Commit history uses the GitHub noreply email.

## Open questions
- Which host (startup-command support decides whether `start.sh` can run automatically).
- First real multiplayer test: claims vs cannons, Lootr per-player chests, Ultimine in claims, nuke lag, Ambush waves.
