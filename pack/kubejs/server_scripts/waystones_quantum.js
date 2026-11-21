// Waystones: every recipe goes through Telejuice (Create: Teleporters' Quantum Fluid).
// Project owner decisions 2026-11-21. See vault/01-Mods/Waystones.md.
//
// Rules applied consistently:
//   1. Ender Pearl -> Quantum Pearl (createwars:quantum_pearl, Ender Pearl + 250 mB Telejuice, mixed)
//   2. Teleport blocks (waystones, sharestones, portstones) get a Quantum Casing on each side of the
//      Warp Stone (Quantum Casing = Railway Casing + 1000 mB Telejuice)
//   3. Paper -> Quantum Paper (createwars:quantum_paper, Paper + 100 mB Telejuice, Spout)
// Exception: Bound Scroll keeps a normal Ender Pearl (owner's call 2026-11-21: only the Warp Scroll's
// pearl was swapped). Its paper is still Quantum Paper.
//
// Base recipes are Create Waystones Recipes' mechanical-crafting versions (they override Waystones' own),
// re-added with only the swaps above; patterns, casings and output counts are otherwise unchanged.
// Untouched: epitaph, twinbound_feather, warp_plate (no pearl/paper), dye recolors, mossy conversions.
// Custom items: startup_scripts/createwars_items.js.

const QPEARL = { item: 'createwars:quantum_pearl' }
const QPAPER = { item: 'createwars:quantum_paper' }
const QCASING = { item: 'createteleporters:quantum_casing' }
const WARP_STONE = { item: 'waystones:warp_stone' }
const PEARL = { item: 'minecraft:ender_pearl' }
const GOLD = { tag: 'c:nuggets/gold' }
const PURPLE = { tag: 'c:dyes/purple' }
const AMETHYST = { item: 'minecraft:amethyst_shard' }
const WARP_DUST = { item: 'waystones:warp_dust' }

// [recipe/output id, casing, brick, count]
const WAYSTONES = [
  ['waystone',                   'create:andesite_casing', 'minecraft:stone_bricks',               2],
  ['mossy_waystone',             'create:copper_casing',   'minecraft:stone_bricks',               2],
  ['sandy_waystone',             'create:brass_casing',    'minecraft:sandstone',                  2], // was stone_bricks x3 upstream
  ['blackstone_waystone',        'create:andesite_casing', 'minecraft:polished_blackstone_bricks', 2],
  ['deepslate_waystone',         'create:andesite_casing', 'minecraft:deepslate_bricks',           2],
  ['end_stone_waystone',         'create:brass_casing',    'minecraft:end_stone_bricks',           2],
  ['mud_bricks_waystone',        'create:andesite_casing', 'minecraft:mud_bricks',                 2],
  ['prismarine_waystone',        'create:copper_casing',   'minecraft:prismarine_bricks',          2],
  ['purpur_waystone',            'create:brass_casing',    'minecraft:purpur_block',               2],
  ['red_nether_bricks_waystone', 'create:andesite_casing', 'minecraft:red_nether_bricks',          2]
]

// Create Waystones Recipes has no white_sharestone recipe, so white is portstone-only.
const SHARESTONE_COLORS = ['black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue', 'light_gray',
  'lime', 'magenta', 'orange', 'pink', 'purple', 'red', 'yellow']
const PORTSTONE_COLORS = SHARESTONE_COLORS.concat(['white'])

ServerEvents.recipes(event => {
  const mech = (id, pattern, key, count) => {
    event.remove({ id: `waystones:${id}` })
    event.custom({
      type: 'create:mechanical_crafting',
      accept_mirrored: false,
      category: 'misc',
      key: key,
      pattern: pattern,
      result: { count: count, id: `waystones:${id}` },
      show_notification: false
    }).id(`createwars:waystones/${id}`)
  }

  // --- Intermediate: Quantum Paper (Quantum Pearl's mixing recipe is in quantum_pearl_recipe.js) ---
  event.custom({
    type: 'create:filling',
    ingredients: [
      { item: 'minecraft:paper' },
      { type: 'neoforge:single', amount: 100, fluid: 'createteleporters:quantum_fluid' }
    ],
    results: [{ id: 'createwars:quantum_paper' }]
  }).id('createwars:filling/quantum_paper')

  // --- Waystones (all stone variants) ---
  WAYSTONES.forEach(w => {
    mech(w[0],
      [' OOO ', 'AAAAA', ' PPP ', ' QSQ ', ' PPP ', 'AAPAA'],
      { A: { item: w[1] }, O: QPEARL, P: { item: w[2] }, S: WARP_STONE, Q: QCASING },
      w[3])
  })

  // --- Sharestones ---
  SHARESTONE_COLORS.forEach(color => {
    mech(`${color}_sharestone`,
      ['AAAAA', 'DPPPD', ' QSQ ', ' PPP ', 'AAPAA'],
      { A: { item: 'create:andesite_casing' }, D: { tag: `c:dyes/${color}` }, P: { item: 'minecraft:stone_bricks' }, S: WARP_STONE, Q: QCASING },
      2)
  })

  // --- Portstones (Warp Stone row was ' DSD '; casings go on the outside) ---
  PORTSTONE_COLORS.forEach(color => {
    mech(`${color}_portstone`,
      ['QDSDQ', ' PPP ', 'AAPAA'],
      { A: { item: 'create:andesite_casing' }, D: { tag: `c:dyes/${color}` }, P: { item: 'minecraft:stone_bricks' }, S: WARP_STONE, Q: QCASING },
      2)
  })

  // --- Warp Stone, shards ---
  mech('warp_stone', [' AAA ', 'GPPPG', 'GPPPG', ' APA '], { A: AMETHYST, G: { tag: 'c:gems/emerald' }, P: QPEARL }, 1)
  mech('deepslate_shard', [' S ', 'DED', ' S '], { D: WARP_DUST, E: QPEARL, S: { item: 'minecraft:cobbled_deepslate' } }, 2)
  mech('dormant_shard', [' A ', 'DED', ' A '], { A: AMETHYST, D: WARP_DUST, E: QPEARL }, 2)

  // --- Warp Dust (vanilla shapeless in Waystones, not overridden by Create Waystones Recipes) ---
  event.remove({ id: 'waystones:warp_dust' })
  event.shapeless(Item.of('waystones:warp_dust', 4), ['createwars:quantum_pearl', 'minecraft:amethyst_shard'])
    .id('createwars:waystones/warp_dust')

  // --- Scrolls ---
  mech('blank_scroll',  ['GGGGG', 'DPPPD', 'D P D', 'GGPGG'], { G: GOLD, D: PURPLE, P: QPAPER }, 3)
  mech('bound_scroll',  ['DDDDD', 'GPPPG', 'GPEPG', 'DDPDD'], { G: GOLD, D: PURPLE, P: QPAPER, E: PEARL }, 3)
  mech('portal_scroll', ['GGGGG', 'DPPPD', 'DPSPD', 'GGPGG'], { G: GOLD, D: PURPLE, P: QPAPER, S: WARP_STONE }, 3)
  mech('return_scroll', ['GGGGG', 'DPPPD', 'DPPPD', 'GGPGG'], { G: GOLD, D: PURPLE, P: QPAPER }, 3)
  mech('warp_scroll',   ['GGGGG', 'DPPPD', 'DPEPD', 'GGPGG'], { G: GOLD, D: PURPLE, P: QPAPER, E: QPEARL }, 3)
})
