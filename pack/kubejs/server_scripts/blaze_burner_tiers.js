// Blaze burner fuel tiers: Blaze Cake (T1) -> Biofuel (T2) -> Napalm (T3).
// Each tier's fuel needs a superheated burner to produce, so you bootstrap the next tier with the
// previous one. Liquid tiers burn in a Crafts & Additions "Blaze Burner with Straw".
// Design and numbers: vault/03-Design/Blaze Burner Fuel Tiers.md
// KubeJS Create addon is not installed, so these are raw recipe JSON.
ServerEvents.recipes(event => {
  // --- Tier 2: Biofuel needs superheat to brew (was unheated) ---
  event.remove({ id: 'createaddition:mixing/bioethanol' })
  event.custom({
    type: 'create:mixing',
    heat_requirement: 'superheated',
    ingredients: [
      { item: 'minecraft:sugar' },
      { item: 'create:cinder_flour' },
      { item: 'createaddition:biomass' },
      { item: 'createaddition:biomass' }
    ],
    results: [{ amount: 125, id: 'createaddition:bioethanol' }]
  }).id('createwars:mixing/bioethanol_superheated')

  // --- Tier 3: Napalm needs superheat + biofuel (was unheated, aluminum + gasoline only) ---
  event.remove({ id: 'tfmg:mixing/napalm' })
  event.custom({
    type: 'create:mixing',
    heat_requirement: 'superheated',
    ingredients: [
      { tag: 'c:ingots/aluminum' },
      { type: 'neoforge:tag', amount: 1000, tag: 'c:gasoline' },
      { type: 'neoforge:tag', amount: 250, tag: 'c:biofuel' }
    ],
    results: [{ amount: 250, id: 'tfmg:napalm' }]
  }).id('createwars:mixing/napalm_superheated')

  // Napalm as a straw-burner fuel. TFMG's own napalm fuel entry only works with the Create: Liquid
  // Fuel mod, which isn't in the pack. 72000 ticks = 1 hour per bucket (biofuel is 24000 = 20 min).
  event.custom({
    type: 'createaddition:liquid_burning',
    burn_time: 72000,
    ingredients: [{ type: 'neoforge:tag', amount: 1000, tag: 'c:napalm' }],
    results: [],
    superheated: true
  }).id('createwars:liquid_burning/napalm')
})
