// Makes TFMG's Coke Oven and Blast Furnace pollute (Create: Smog built-in model) while they are WORKING.
// Project owner decision 2026-11-21 ("Yes, script it").
// Why a script: Smog's config can only list a block as a source if it has a 'lit' blockstate to switch
// it on and off. TFMG's machines have none, so a config entry would pollute even when idle. PoTR's own
// TFMG hooks are outdated (vault/02-Bugs/PoTR coremod misses TFMG coke oven and blast furnace.md).
// "Working" = the block entity's public `currentRecipe` is set (Coke Oven: controller block only;
// Blast Furnace: also needs fuel). Checked with javap against tfmg-1.21.1-1.3.3a-community.
// Limitation: Smog.add puts pollution straight into the chunk, so smokestacks can't vent it. Scrubbers
// and precipitators still clean it.
// Uses only already-loaded chunks near players, so it never loads chunks.
const TFMG_SMOG_INTERVAL = 100   // ticks between checks (5 s), same as Smog's own tickInterval
const TFMG_SMOG_CHUNK_RADIUS = 8 // chunks around each player
// pollution per second while working, split into Smog's three kinds (soot, fumes, sulfur)
const TFMG_SMOG_RATES = {
  'block.tfmg.coke_oven': { soot: 18, fumes: 6, sulfur: 6 },
  'block.tfmg.blast_furnace_output': { soot: 24, fumes: 18, sulfur: 18 }
}
let tfmgSmogErrorLogged = false

function tfmgSmogIsWorking(be, key) {
  if (be.currentRecipe == null) return false
  if (key == 'block.tfmg.coke_oven') return be.isController()
  return be.fuel > 0
}

function tfmgSmogScanChunk(level, cx, cz, seen, seconds) {
  const key = cx + ',' + cz
  if (seen[key]) return
  seen[key] = true
  const chunk = level.getChunkSource().getChunkNow(cx, cz)
  if (chunk == null) return
  chunk.getBlockEntities().values().forEach(be => {
    const id = String(be.getBlockState().getBlock().getDescriptionId())
    const rates = TFMG_SMOG_RATES[id]
    if (!rates || !tfmgSmogIsWorking(be, id)) return
    const pos = be.getBlockPos()
    Smog.add(level, pos, 'soot', rates.soot * seconds)
    Smog.add(level, pos, 'fumes', rates.fumes * seconds)
    Smog.add(level, pos, 'sulfur', rates.sulfur * seconds)
  })
}

ServerEvents.tick(event => {
  const server = event.server
  if (server.tickCount % TFMG_SMOG_INTERVAL != 0) return
  const seconds = TFMG_SMOG_INTERVAL / 20
  try {
    server.allLevels.forEach(level => {
      const seen = {}
      level.players.forEach(player => {   // KubeJS: a list property, not a method
        const pcx = player.blockX >> 4
        const pcz = player.blockZ >> 4
        for (let cx = pcx - TFMG_SMOG_CHUNK_RADIUS; cx <= pcx + TFMG_SMOG_CHUNK_RADIUS; cx++) {
          for (let cz = pcz - TFMG_SMOG_CHUNK_RADIUS; cz <= pcz + TFMG_SMOG_CHUNK_RADIUS; cz++) {
            tfmgSmogScanChunk(level, cx, cz, seen, seconds)   // Rhino: no const inside loop bodies
          }
        }
      })
    })
  } catch (e) {
    if (!tfmgSmogErrorLogged) {
      console.error('[createwars] tfmg_smog_sources.js failed, TFMG pollution is off: ' + e)
      tfmgSmogErrorLogged = true
    }
  }
})
