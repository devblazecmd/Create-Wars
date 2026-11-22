// One wire and one empty spool (owner 2026-11-22: "pick one set to be primary" -> Create Crafts and Additions).
// See vault/03-Design/Metal Unification.md (Wire and spool section).
//   Copper wire: C&A's, made only in the Rolling Mill. TFMG's ingot-stonecutter wire and The Air War's crafted
//                "Wires" are removed and hidden; recipes that used them take #c:wires/copper.
//   Empty spool: C&A's (iron). TFMG's wooden empty spool is removed and hidden; TFMG's copper/aluminum/constantan
//                spools are wound on the C&A spool instead.
//   Copper spools stay separate: each is the wiring TOOL for its own mod's network (C&A connectors vs TFMG cable
//   insulators). They are renamed in kubejs/assets/*/lang/en_us.json so players can tell them apart.
const WIRE_HIDDEN = ['tfmg:copper_wire', 'create_the_air_wars:wires', 'tfmg:empty_spool']

ServerEvents.recipes(event => {
  event.remove({ id: 'tfmg:copper_wire_from_ingots_copper_stonecutting' })
  event.remove({ id: 'create_the_air_wars:wires' })
  event.remove({ id: 'tfmg:empty_spool_from_hardened_planks_stonecutting' })
  event.replaceInput({ input: 'tfmg:copper_wire' }, 'tfmg:copper_wire', '#c:wires/copper')
  event.replaceInput({ input: 'create_the_air_wars:wires' }, 'create_the_air_wars:wires', '#c:wires/copper')
  event.replaceInput({ input: 'tfmg:empty_spool' }, 'tfmg:empty_spool', 'createaddition:spool')
})

ServerEvents.tags('item', event => {
  event.add('c:hidden_from_recipe_viewers', WIRE_HIDDEN)
})
