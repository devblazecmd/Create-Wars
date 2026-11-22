// One steel for the whole pack. Project owner decision 2026-11-21: "All interchangeable".
// Three mods each add steel: TFMG (tfmg:), Create Big Cannons (createbigcannons:) and Create: Gunsmithing
// (cgs:). All three already tag their items into the shared c: tags, so:
//   1. Every recipe that asks for a specific steel item now accepts the c: tag (any mod's steel works).
//   2. Every recipe that makes CBC or Gunsmithing steel makes TFMG steel instead (TFMG is the main
//      steel: its blast furnace line exists to make it).
//   3. CBC and Gunsmithing steel are hidden from JEI. Copies already in a world still work everywhere,
//      because they keep their c: tags.
// See vault/03-Design/Steel Unification.md.
const STEEL_FORMS = [
  // [c: tag, TFMG item (the one kept), other mods' items]
  ['c:ingots/steel', 'tfmg:steel_ingot', ['createbigcannons:steel_ingot', 'cgs:steel_ingot']],
  ['c:nuggets/steel', 'tfmg:steel_nugget', ['cgs:steel_nugget']],   // CBC has no steel nugget item
  ['c:storage_blocks/steel', 'tfmg:steel_block', ['createbigcannons:steel_block', 'cgs:steel_block']]
]

ServerEvents.recipes(event => {
  STEEL_FORMS.forEach(form => {
    const tag = form[0], main = form[1], others = form[2]
    // inputs: any steel
    ;[main].concat(others).forEach(id => event.replaceInput({ input: id }, id, '#' + tag))
    // outputs: always TFMG steel
    others.forEach(id => event.replaceOutput({ output: id }, id, main))
  })
  // Steel sheets: only make recipes accept any steel plate (both mods tag theirs as c:plates/steel).
  event.replaceInput({ input: 'cgs:steel_sheet' }, 'cgs:steel_sheet', '#c:plates/steel')
})

ServerEvents.tags('item', event => {
  STEEL_FORMS.forEach(form => event.add('c:hidden_from_recipe_viewers', form[2]))
})
