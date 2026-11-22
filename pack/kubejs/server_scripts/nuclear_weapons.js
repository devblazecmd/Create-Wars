// Nuclear weapons from CBC Enhanced Shells (cbc_enhanced_shells), gated behind Create Nuclear.
// Project owner decision 2026-11-22: add the nuke shells, make them cost reactor-grade uranium, and hide the
// mod's other ~100 shells (they overlap CBC Military Supplement and Create: Warnautics).
// See vault/03-Design/Nuclear Weapons.md.
//
// Only these four items stay. The H-bombs keep the mod's own recipes because they are built from nuke shells.
const CBCES_KEEP = [
  'cbc_enhanced_shells:nuke_shell',
  'cbc_enhanced_shells:nuke_shell_mk2',
  'cbc_enhanced_shells:h_bomb_shell',
  'cbc_enhanced_shells:h_bomb_mini_shell'
]

// Pinned to 1.2.5, not the newest, because CBC: Firepower Components 0.4.4 refuses to load with
// cbc_enhanced_shells outside [1.2.2,1.3.0). Everything is matched by mod ID, not a hardcoded item list,
// so this keeps working when either mod updates.
ServerEvents.recipes(event => {
  // Drop every recipe from the mod except the two H-bombs (built from nuke shells, already gated).
  event.remove({ mod: 'cbc_enhanced_shells', not: [
    { id: 'cbc_enhanced_shells:h_bomb_shell' }, { id: 'cbc_enhanced_shells:h_bomb_mini_shell' }] })

  // Nuke Mk.I: a CBC HE shell wrapped in uranium fuel rods and lead shielding, with a nether star core.
  // Uranium rods need enriched yellowcake, i.e. Create Nuclear's full refining line.
  event.custom({
    type: 'create:mechanical_crafting',
    accept_mirrored: false,
    category: 'misc',
    pattern: [
      ' LLL ',
      'LUUUL',
      'LUNUL',
      'LUUUL',
      ' LHL '
    ],
    key: {
      L: { tag: 'c:ingots/lead' },
      U: { item: 'createnuclear:uranium_rod' },
      N: { item: 'minecraft:nether_star' },
      H: { item: 'createbigcannons:he_shell' }
    },
    result: { id: 'cbc_enhanced_shells:nuke_shell', count: 1 }
  }).id('createwars:nuke_shell')

  // Nuke Mk.II: a Mk.I boosted with thorium and enriched yellowcake.
  event.custom({
    type: 'create:mechanical_crafting',
    accept_mirrored: false,
    category: 'misc',
    pattern: [
      ' TYT ',
      'TUUUT',
      'YUMUY',
      'TUUUT',
      ' TYT '
    ],
    key: {
      T: { item: 'createnuclear:thorium_rod' },
      Y: { item: 'createnuclear:enriched_yellowcake' },
      U: { item: 'createnuclear:uranium_rod' },
      M: { item: 'cbc_enhanced_shells:nuke_shell' }
    },
    result: { id: 'cbc_enhanced_shells:nuke_shell_mk2', count: 1 }
  }).id('createwars:nuke_shell_mk2')
})

ServerEvents.tags('item', event => {
  event.add('c:hidden_from_recipe_viewers', /^cbc_enhanced_shells:/)
  event.remove('c:hidden_from_recipe_viewers', CBCES_KEEP)
})
