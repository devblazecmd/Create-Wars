// Recipes for items that shipped with none (found by tools/audit_quests.py 2026-11-22).
// Owner 2026-11-22: "fix those item give them recipes". See vault/02-Bugs/Quest items with no survival recipe.md.
// Rhino note: no const/let inside nested blocks (loop bodies); use top-level helper functions.

// ---------------------------------------------------------------------------------------------------------------
// Create: Armored Constructs (arcon 1.0.0 ships with no recipes at all).
// Six hull armors. Cost follows the mod's own stats (data/arcon/block_armor/tags): toughness / mass
//   aluminum 4 / 0.25, titanium 6 / 0.5   (light: aircraft)
//   rolled 15 / 2, nickel 22 / 2.5, ceramic 34 / 1.2, boron 48 / 1.5   (heavy: ground vehicles)
// Each base recipe makes one colour; a stonecutter turns any hull into any colour of the same material.
const ARCON_COLOURS_GROUND = ['dark', 'desert', 'forest', 'green', 'snow', 'brown', 'sand_green', 'green_gray', 'urban',
  'faded_khaki', 'factory', 'eastern_european', 'polar_blue', 'shadow_violet_gray', 'cobalt_operational']
const ARCON_COLOURS_AIR = ['light_ghost_gray', 'dark_ghost_gray', 'gunship_gray', 'neutral_gray', 'flanker_light_blue',
  'flanker_medium_blue', 'flanker_dark_blue', 'olive_drab', 'forest_green', 'aviation_green', 'desert_sand', 'dark_tan',
  'insignia_white', 'radome_green', 'matte_black']
const ARCON_HULLS = {
  aluminum: ARCON_COLOURS_AIR, titanium: ARCON_COLOURS_AIR,
  rolled: ARCON_COLOURS_GROUND, nickel: ARCON_COLOURS_GROUND, ceramic: ARCON_COLOURS_GROUND, boron: ARCON_COLOURS_GROUND
}
// Kept hidden: marked "(in development)" by the mod itself, or creative-tab banner pieces.
const ARCON_HIDDEN = ['thermal_vision_module', 'power_generator', 'aiming_module', 'optical_observation_unit',
  'kontakt_1_black', 'kontakt_1_desert', 'kontakt_1_forest', 'kontakt_1_green', 'kontakt_1_snow', 'kontakt_1_platform',
  'banner_part_1', 'banner_part_2', 'banner_part_3', 'banner_part_4', 'banner_part_5',
  'banner_part_6', 'banner_part_7', 'banner_part_8', 'banner_part_9'].map(id => 'arcon:' + id)

function arconHullStonecutting(event, material) {
  ARCON_HULLS[material].forEach(colour => {
    event.stonecutting('arcon:hull_' + material + '_' + colour, '#createwars:arcon_hull_' + material)
      .id('createwars:arcon/hull_' + material + '_' + colour)
  })
}

function mechCrafting(event, id, result, count, pattern, key) {
  event.custom({
    type: 'create:mechanical_crafting', accept_mirrored: false, category: 'misc',
    pattern: pattern, key: key, result: { id: result, count: count }
  }).id('createwars:' + id)
}

ServerEvents.recipes(event => {
  // --- hull armor: base recipes (8 blocks each) ---
  event.shaped(Item.of('arcon:hull_aluminum_neutral_gray', 8), ['AAA', 'ASA', 'AAA'],
    { A: 'tfmg:aluminum_sheet', S: '#c:plates/steel' }).id('createwars:arcon/hull_aluminum')
  event.shaped(Item.of('arcon:hull_titanium_neutral_gray', 8), ['TTT', 'TAT', 'TTT'],
    { T: 'create_the_air_wars:titaniumsheet', A: 'tfmg:aluminum_sheet' }).id('createwars:arcon/hull_titanium')
  event.shaped(Item.of('arcon:hull_rolled_green', 8), ['SPS', 'PHP', 'SPS'],
    { S: '#c:ingots/steel', P: '#c:plates/steel', H: 'tfmg:heavy_plate' }).id('createwars:arcon/hull_rolled')
  event.shaped(Item.of('arcon:hull_nickel_green', 8), ['NHN', 'HSH', 'NHN'],
    { N: 'tfmg:nickel_ingot', H: 'tfmg:heavy_plate', S: '#c:storage_blocks/steel' }).id('createwars:arcon/hull_nickel')
  event.shaped(Item.of('arcon:hull_ceramic_green', 8), ['FHF', 'HDH', 'FHF'],
    { F: 'tfmg:fireclay', H: 'tfmg:heavy_plate', D: 'minecraft:diamond' }).id('createwars:arcon/hull_ceramic')
  mechCrafting(event, 'arcon/hull_boron', 'arcon:hull_boron_green', 8,
    ['CHC', 'HNH', 'CHC'],
    { C: { item: 'tfmg:coal_coke' }, H: { item: 'tfmg:heavy_plate' }, N: { item: 'minecraft:netherite_scrap' } })
  Object.keys(ARCON_HULLS).forEach(m => arconHullStonecutting(event, m))

  // --- tank gun: breech -> barrel(s) -> intermediate muzzle -> muzzle ---
  mechCrafting(event, 'arcon/barrel_section', 'arcon:arcon_barrel_section', 1,
    ['HPH', 'SMS', 'HPH'],
    { H: { item: 'tfmg:heavy_plate' }, P: { tag: 'c:plates/steel' }, S: { tag: 'c:storage_blocks/steel' },
      M: { item: 'tfmg:steel_mechanism' } })
  mechCrafting(event, 'arcon/cannon_barrel', 'arcon:arcon_cannon_barrel', 2,
    ['HSH', 'H H', 'HSH'],
    { H: { item: 'tfmg:heavy_plate' }, S: { tag: 'c:ingots/steel' } })
  mechCrafting(event, 'arcon/intermediate_muzzle', 'arcon:arcon_intermediate_muzzle', 1,
    ['PSP', 'S S', 'PSP'],
    { P: { tag: 'c:plates/steel' }, S: { tag: 'c:ingots/steel' } })
  mechCrafting(event, 'arcon/cannon_muzzle', 'arcon:arcon_cannon_muzzle', 1,
    ['P P', 'HSH', 'P P'],
    { P: { tag: 'c:plates/steel' }, H: { item: 'tfmg:heavy_plate' }, S: { tag: 'c:ingots/steel' } })
  // BOPS round: an AP shot in a brass case. Firing leaves a Spent Cartridge Casing, which can be reloaded.
  event.shapeless('arcon:bops', ['createbigcannons:ap_shot', 'create:brass_sheet', 'create:brass_sheet',
    'createbigcannons:packed_guncotton']).id('createwars:arcon/bops')
  event.shapeless('arcon:bops', ['createbigcannons:ap_shot', 'arcon:cartridge', 'createbigcannons:packed_guncotton'])
    .id('createwars:arcon/bops_reload')
  // fire control: the Rangefinder block has no item form in 1.0.0 (not in the item registry), so no recipe.
  event.shaped('arcon:steel_seat', [' W ', 'PPP'], { W: '#minecraft:wool', P: '#c:plates/steel' })
    .id('createwars:arcon/steel_seat')

  // ---------------------------------------------------------------------------------------------------------
  // CBC Military Supplement 3.0.7: items with a loot table but no recipe.
  // Rocket Bracket is also an ingredient of the Dual HE/APHE rockets (cbcmoreshells_fixes.js).
  event.shaped(Item.of('cbcmoreshells:rocket_bracket', 2), ['B B', 'SSS'],
    { B: 'minecraft:iron_bars', S: 'create:iron_sheet' }).id('createwars:cbcms/rocket_bracket')
  event.shaped('cbcmoreshells:he_bouncing_bomb', ['SGS', 'GFG', 'SGS'],
    { S: 'create:iron_sheet', G: 'createbigcannons:packed_guncotton', F: 'createbigcannons:impact_fuze' })
    .id('createwars:cbcms/he_bouncing_bomb')
  event.shaped('cbcmoreshells:aphe_bouncing_bomb', ['SCS', 'GFG', 'SGS'],
    { S: 'create:iron_sheet', C: '#c:ingots/cast_iron', G: 'createbigcannons:packed_guncotton',
      F: 'createbigcannons:impact_fuze' }).id('createwars:cbcms/aphe_bouncing_bomb')
  event.shaped('cbcmoreshells:depth_charge', ['SGS', 'GFG', 'SGS'],
    { S: 'create:iron_sheet', G: 'createbigcannons:packed_guncotton', F: 'createbigcannons:timed_fuze' })
    .id('createwars:cbcms/depth_charge')
  // aerial torpedo: a basic torpedo fitted to a bracket for aircraft racks
  event.shapeless('cbcmoreshells:racked_torpedo', ['cbcmoreshells:primary_torpedo', 'cbcmoreshells:rocket_bracket',
    'create:iron_sheet', 'create:iron_sheet']).id('createwars:cbcms/racked_torpedo')
  // a hydrophone
  event.shaped('cbcmoreshells:torpedo_detection_device', ['CTC', 'CNC', ' B '],
    { C: 'create:copper_sheet', T: 'create:electron_tube', N: 'minecraft:note_block', B: 'create:brass_casing' })
    .id('createwars:cbcms/torpedo_detection_device')

  // ---------------------------------------------------------------------------------------------------------
  // Synaxis 1.6.3: jet engine + rudder. Late game: TFMG turbine blades.
  mechCrafting(event, 'synaxis/jet', 'synaxis:jet', 1,
    ['PTP', 'TBT', 'PFP'],
    { P: { tag: 'c:plates/steel' }, T: { item: 'tfmg:turbine_blade' }, B: { item: 'create:blaze_burner' },
      F: { item: 'create:fluid_pipe' } })
  event.shaped('synaxis:jet_rudder', ['P P', 'PSP'], { P: '#c:plates/steel', S: 'create:shaft' })
    .id('createwars:synaxis/jet_rudder')

  // ---------------------------------------------------------------------------------------------------------
  // Create: The Air War 5.00: FPV drone + its joystick.
  event.shaped('create_the_air_wars:fpv_drone', ['PGP', 'ACA', 'PKP'],
    { P: 'aeronautics:andesite_propeller', G: 'create_the_air_wars:gyro_stabilizer', A: 'create_the_air_wars:antenna',
      C: 'create_the_air_wars:camera', K: 'createbigcannons:packed_guncotton' }).id('createwars:airwar/fpv_drone')
  event.shaped('create_the_air_wars:drone_controller', ['BAB', 'BMB', 'BTB'],
    { B: 'create:brass_sheet', A: 'create_the_air_wars:antenna', M: 'create_the_air_wars:monitor',
      T: 'create:electron_tube' }).id('createwars:airwar/drone_controller')
})

ServerEvents.tags('item', event => {
  Object.keys(ARCON_HULLS).forEach(m => {
    event.add('createwars:arcon_hull_' + m, ARCON_HULLS[m].map(c => 'arcon:hull_' + m + '_' + c))
  })
  event.add('c:hidden_from_recipe_viewers', ARCON_HIDDEN)
})
