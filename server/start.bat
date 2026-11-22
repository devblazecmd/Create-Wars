@echo off
rem Create Wars server start: update mods/configs from GitHub, then start NeoForge.
set PACK_URL=https://raw.githubusercontent.com/devblazecmd/Create-Wars/main/pack/pack.toml
if not exist packwiz-installer-bootstrap.jar (
  curl -L -o packwiz-installer-bootstrap.jar "https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar"
)
java -jar packwiz-installer-bootstrap.jar -g -s server "%PACK_URL%"
call run.bat nogui
