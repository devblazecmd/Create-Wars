// Renewable netherite: crush Nether Bricks (block) for a small chance of Netherite Scrap.
// Project owner request 2026-11-21. See vault/03-Design/Netherite Scrap Crushing.md.
// Netherrack is infinite -> smelt to nether brick items -> craft blocks -> crush. One ingot
// (4 scrap) takes ~80 blocks (~320 netherrack) at 5% (owner raised it from 2% on 2026-11-21).
// Tune NETHERITE_SCRAP_CHANCE to balance. No other recipe crushes nether bricks (checked 2026-11-21).
const NETHERITE_SCRAP_CHANCE = 0.05

ServerEvents.recipes(event => {
  event.custom({
    type: 'create:crushing',
    ingredients: [{ item: 'minecraft:nether_bricks' }],
    processing_time: 250,
    results: [
      { id: 'minecraft:nether_brick', count: 2 },
      { id: 'minecraft:netherite_scrap', chance: NETHERITE_SCRAP_CHANCE }
    ]
  }).id('createwars:crushing/netherite_scrap_from_nether_bricks')
})
