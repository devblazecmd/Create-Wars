// AMBUSH grace period and raid gap (owner 2026-11-23: "ambush needs a grace period starting fresh hitting raids are
// very hard to fight"; "10hrs of real playtime"; "there NEEDS to be time between raids so they cant spawn back to back",
// "2hrs").
//
// AMBUSH (ambush-1.1.8) has no grace setting, but it has one server-wide switch for natural ambushes:
// `/ambush admin spawning` toggles it and returns the NEW state (1 = on, 0 = off; read from the bytecode of
// AmbushRuntime.toggleNaturalSpawning). It is saved with the world. Quest-started ambushes (Defend Your Home waves)
// ignore it, so only random ambushes and natural airships are held back.
//
// This script keeps that switch OFF:
//   * for the first 10 hours of play on a world (play time = server ticks while at least one player is online, so an
//     empty server doesn't use the grace up), and
//   * while any AMBUSH mob is alive (they carry the `ambush_owned` tag) and for 2 hours of play after the last one is
//     gone, so raids can't come back to back.
// Otherwise it turns the switch ON. State lives in the server's persistent data (saved with the world).
// Rhino note: no const/let inside nested blocks; use var.

const AMBUSH_GRACE_TICKS = 10 * 60 * 60 * 20     // 10 hours of play
const AMBUSH_GAP_TICKS = 2 * 60 * 60 * 20        // 2 hours of play after an ambush ends
const AMBUSH_CHECK_EVERY = 200                   // ticks (10 s)
const AMBUSH_KEY_PLAY = 'createwars_ambush_play_ticks'
const AMBUSH_KEY_GAP_UNTIL = 'createwars_ambush_gap_until'
const AMBUSH_KEY_GRACE_DONE = 'createwars_ambush_grace_announced'

let ambushApplied = null      // the state this script last set (null = not yet this session, so set it once)
let ambushErrorLogged = false

function ambushSetNatural(server, want) {
  // Toggle, and toggle again if it landed on the wrong state: the command only toggles.
  var r = server.runCommandSilent('ambush admin spawning')
  if ((r == 1) != want) r = server.runCommandSilent('ambush admin spawning')
  ambushApplied = want
  console.info('[createwars] AMBUSH natural spawning ' + (want ? 'ON' : 'OFF') + ' (toggle result ' + r + ')')
}

function ambushHours(ticks) {
  return Math.ceil(ticks / 72000 * 10) / 10
}

ServerEvents.tick(event => {
  const server = event.server
  if (server.tickCount % AMBUSH_CHECK_EVERY != 0) return
  try {
    var data = server.persistentData
    var play = data.getLong(AMBUSH_KEY_PLAY)
    var online = server.getPlayerList().getPlayerCount()
    if (online > 0) {
      play = play + AMBUSH_CHECK_EVERY
      data.putLong(AMBUSH_KEY_PLAY, play)
    }
    // `execute if entity` returns how many matched; > 0 while an ambush is running somewhere
    var active = server.runCommandSilent('execute if entity @e[tag=ambush_owned]') > 0
    var gapUntil = data.getLong(AMBUSH_KEY_GAP_UNTIL)
    if (active && gapUntil < play + AMBUSH_GAP_TICKS) {
      gapUntil = play + AMBUSH_GAP_TICKS
      data.putLong(AMBUSH_KEY_GAP_UNTIL, gapUntil)
    }
    var inGrace = play < AMBUSH_GRACE_TICKS
    var want = !inGrace && !active && play >= gapUntil
    if (ambushApplied !== want) ambushSetNatural(server, want)
    if (!inGrace && !data.getBoolean(AMBUSH_KEY_GRACE_DONE)) {
      data.putBoolean(AMBUSH_KEY_GRACE_DONE, true)
      server.tell(Text.of('The grace period is over: ambushes and raiding airships can now find your base.').red())
    }
  } catch (e) {
    if (!ambushErrorLogged) {
      console.error('[createwars] ambush_grace.js failed: ' + e)
      ambushErrorLogged = true
    }
  }
})

PlayerEvents.loggedIn(event => {
  try {
    var play = event.server.persistentData.getLong(AMBUSH_KEY_PLAY)
    if (play < AMBUSH_GRACE_TICKS) {
      event.player.tell(Text.of('Grace period: no random ambushes for about ' + ambushHours(AMBUSH_GRACE_TICKS - play) +
        ' more hours of play. Build your defenses.').gold())
    }
  } catch (e) {
    console.error('[createwars] ambush_grace.js login message failed: ' + e)
  }
})
