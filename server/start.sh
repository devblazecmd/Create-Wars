#!/usr/bin/env sh
# Create Wars server start: update mods/configs from GitHub, then start NeoForge.
# Run from the server folder (the one with run.sh after the NeoForge installer has run).
set -e
PACK_URL="https://raw.githubusercontent.com/devblazecmd/Create-Wars/main/pack/pack.toml"
if [ ! -f packwiz-installer-bootstrap.jar ]; then
  curl -L -o packwiz-installer-bootstrap.jar "https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar"
fi
# -g: no GUI, -s server: skip client-only mods (Sodium, Iris, ...)
java -jar packwiz-installer-bootstrap.jar -g -s server "$PACK_URL"
exec sh ./run.sh nogui
