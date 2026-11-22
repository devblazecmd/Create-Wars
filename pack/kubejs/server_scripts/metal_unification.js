// One of each metal for the whole pack. Several mods add the same metal; the extra copies are folded into one.
// See vault/03-Design/Metal Unification.md.
//   Steel: owner 2026-11-21 "All interchangeable". TFMG, Create Big Cannons, Create: Gunsmithing (cgs) and
//          Create Nuclear (added 2026-11-22) each add steel.
//   Lead:  owner 2026-11-22 "unify lead the same way as steel". TFMG, Gunsmithing and Create Nuclear each add
//          lead. Only TFMG's lead ore still generates (kubejs/data/{cgs,createnuclear}/neoforge/biome_modifier).
//   Uranium: checked 2026-11-22, only Create Nuclear adds it (create:crushed_raw_uranium is Create's own
//          compat intermediate that Create Nuclear's chain uses), so nothing to unify.
// For every form:
//   1. Every recipe that asks for a specific item now accepts the c: tag (any mod's copy works).
//   2. Every recipe that makes another mod's copy makes the TFMG one instead.
//   3. The other copies are hidden from JEI, and added to the c: tag in case their mod forgot (Gunsmithing's lead
//      block and Create Nuclear's raw lead block had no item tag), so copies already in a world still work.
const METAL_FORMS = [
  // [c: tag, TFMG item (the one kept), other mods' items]
  ['c:ingots/steel', 'tfmg:steel_ingot', ['createbigcannons:steel_ingot', 'cgs:steel_ingot', 'createnuclear:steel_ingot']],
  ['c:nuggets/steel', 'tfmg:steel_nugget', ['cgs:steel_nugget', 'createnuclear:steel_nugget']],   // CBC has no steel nugget
  ['c:storage_blocks/steel', 'tfmg:steel_block', ['createbigcannons:steel_block', 'cgs:steel_block', 'createnuclear:steel_block']],
  ['c:ingots/lead', 'tfmg:lead_ingot', ['cgs:lead_ingot', 'createnuclear:lead_ingot']],
  ['c:nuggets/lead', 'tfmg:lead_nugget', ['cgs:lead_nugget', 'createnuclear:lead_nugget']],
  ['c:storage_blocks/lead', 'tfmg:lead_block', ['cgs:lead_block', 'createnuclear:lead_block']],
  ['c:raw_materials/lead', 'tfmg:raw_lead', ['cgs:raw_lead', 'createnuclear:raw_lead']],
  ['c:storage_blocks/raw_lead', 'tfmg:raw_lead_block', ['cgs:raw_lead_block', 'createnuclear:raw_lead_block']]
]
// Ore blocks: no recipe makes them, so they are only tagged and hidden (they no longer generate in new chunks).
const HIDDEN_LEAD_ORES = ['cgs:lead_ore', 'cgs:deepslate_lead_ore', 'createnuclear:lead_ore', 'createnuclear:deepslate_lead_ore']

ServerEvents.recipes(event => {
  METAL_FORMS.forEach(form => {
    const tag = form[0], main = form[1], others = form[2]
    // inputs: any mod's copy
    ;[main].concat(others).forEach(id => event.replaceInput({ input: id }, id, '#' + tag))
    // outputs: always TFMG's
    others.forEach(id => event.replaceOutput({ output: id }, id, main))
  })
  // Owner 2026-11-22: Create Nuclear's mixer steel (iron + coal dust, NO heat) skipped the heat progression.
  // Early steel stays heated (CBC) or superheated (Gunsmithing); TFMG's blast furnace is the bulk route.
  event.remove({ id: 'createnuclear:mixing/steel' })
  // Steel sheets: only make recipes accept any steel plate (both mods tag theirs as c:plates/steel).
  event.replaceInput({ input: 'cgs:steel_sheet' }, 'cgs:steel_sheet', '#c:plates/steel')
})

ServerEvents.tags('item', event => {
  METAL_FORMS.forEach(form => {
    event.add(form[0], form[2])
    event.add('c:hidden_from_recipe_viewers', form[2])
  })
  event.add('c:ores/lead', HIDDEN_LEAD_ORES)
  event.add('c:hidden_from_recipe_viewers', HIDDEN_LEAD_ORES)
})
