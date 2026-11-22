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

## UltraServers (owner, 2026-11-22)
- NeoForge server type via **Change Version**; custom startup scripts need a **support ticket** (docs). So the first test
  uses an uploaded bundle (`-s server` install zipped: 123 mods, config, kubejs; 283 MB), and auto-update waits for a ticket.
- **Blocker found:** CBC Aeronautics Missiles (`cbcaeronauticsmissiles-0.2.0.jar`, CurseForge file 8746555) is excluded from
  the CurseForge API and is All Rights Reserved. Fresh installs stop and ask for a manual download. Owner's own instance
  only had it from an earlier manual download. The server bundle includes it; each player downloads it once.
  Alternatives if that's too annoying: replace it (Modrinth's Create Missiles is a different, GPL mod) or drop it.
- NeoForge: 21.1.267 is the newest 1.21.1 build. Newer NeoForge (26.1.x) is a different Minecraft version, and Create,
  Aeronautics, Big Cannons, Sable, TFMG, Create Nuclear and Radars have no builds past 1.21.1 (checked 2026-11-22).

## Open questions
- Which host (startup-command support decides whether `start.sh` can run automatically).
- First real multiplayer test: claims vs cannons, Lootr per-player chests, Ultimine in claims, nuke lag, Ambush waves.
