// Disables Pollution of the Realms' own pollution-handling tools. Create: Smog's machines (smokestacks,
// ducts, precipitator, air scrubbers, respirator, sensor, aerometer) are the pack's only way to deal with
// pollution. Project owner decision 2026-11-21: "i want it all disabled and create to be the standard".
// PoTR still makes the pollution (carbon/sulfur/dust blocks, polluted water); Smog runs in
// POTR_AND_BUILT_IN mode and cleans it. See vault/01-Mods/Pollution of the Realms.md.
// Recipes are removed and the items hidden from JEI (c:hidden_from_recipe_viewers). Items that already
// exist in a world, or come from /give or creative, are not deleted.
const POTR_TOOLS = [
  'adpother:aerometer',            // Smog has its own Aerometer
  'adpother:iron_filter_frame',
  'adpother:gold_filter_frame',
  'adpother:diamond_filter_frame',
  'adpother:iron_vacuum_bag',
  'adpother:gold_vacuum_bag',
  'adpother:diamond_vacuum_bag',
  'adpother:iron_vacuum_tube',
  'adpother:gold_vacuum_tube',
  'adpother:diamond_vacuum_tube',
  'adpother:iron_respirator',      // Smog has its own Respirator
  'adpother:gold_respirator',
  'adpother:diamond_respirator'
]

ServerEvents.recipes(event => {
  POTR_TOOLS.forEach(id => event.remove({ output: id }))
  event.remove({ mod: 'adpother' })   // catches the filter_change recipe and anything added later
})

ServerEvents.tags('item', event => {
  event.add('c:hidden_from_recipe_viewers', POTR_TOOLS)
})
