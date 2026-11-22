# Create Wars: server and friends setup

Pack URL (works once the GitHub repo is public):
`https://raw.githubusercontent.com/devblazecmd/Create-Wars/main/pack/pack.toml`

Versions: Minecraft **1.21.1**, NeoForge **21.1.267**, Java **21**. RAM: **10-12 GB** for the server.

## Server (rented host)
1. Make a **NeoForge 1.21.1** server, version **21.1.267** (most hosts have a NeoForge option/egg; otherwise upload the
   NeoForge installer and run `java -jar neoforge-21.1.267-installer.jar --installServer`).
2. Start it once so it creates its files, then stop it. Accept the EULA (`eula=true` in `eula.txt`).
3. Upload `start.sh` (Linux hosts; `start.bat` on Windows) and `user_jvm_args.txt` from this folder into the
   server's main folder (next to `run.sh`).
4. Set the host's startup command to run the script: `sh start.sh`. If the host only lets you pick a jar, run the
   packwiz line from `start.sh` once by hand (console/SSH) before each start instead.
5. Apply `server.properties.recommended` to `server.properties`. **`allow-flight=true` is required.**
6. Start it. First start downloads ~220 mods. Add friends: `/whitelist add <name>`, and `/op <you>`.

Every restart pulls the latest pack from GitHub, so a fix pushed to `main` reaches the server on its next restart.

## Each player (Prism Launcher)
1. Add Instance -> Minecraft **1.21.1**, loader **NeoForge 21.1.267**.
2. Download `packwiz-installer-bootstrap.jar`
   (https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar)
   into the instance's `minecraft` folder (Instance -> Folder -> `minecraft`).
3. Edit Instance -> Settings -> Custom commands -> tick it, and set **Pre-launch command** to:
   `"$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/devblazecmd/Create-Wars/main/pack/pack.toml`
4. Settings -> Java -> Memory: max **8 GB** (6 minimum).
5. Launch. The first launch downloads everything (a window shows progress), and every launch after that updates.

## Notes
- The quest book comes from the pack. Don't edit it in game: changes are overwritten on the next update.
- `kubejs/server_scripts/export_registry_ids.js` writes two JSON files at startup (dev tool for the quest checker);
  harmless on a server.
