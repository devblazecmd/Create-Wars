// Fixes for CBC Military Supplement (namespace cbcmoreshells) upstream bugs. Owner approved 2026-11-21.
// 1. Dual HE / Dual APHE rocket recipes use the pre-1.21 result format ({"item": ...}) and fail to load,
//    so the items were uncraftable. Same recipe (rocket + bracket + rocket), rebuilt in the 1.21 format.
// 2. Block loot tables: kubejs/data/cbcmoreshells/loot_table/blocks/*.json override 11 upstream tables that
//    use minecraft:copy_nbt (removed in 1.21), so those blocks dropped nothing. Rewritten in CBC 5.11.7's own
//    1.21 format (copy_components with createbigcannons:tracer and :fuze). Do NOT put notes/README files in
//    kubejs/data: every file there is a resource, and uppercase names are an error.
// See vault/02-Bugs/Cross-mod compat noise on server boot.md. Delete when upstream fixes it.
ServerEvents.recipes(event => {
  event.shaped('cbcmoreshells:dual_he_rocket', ['RBR'], {
    R: 'cbcmoreshells:he_rocket',
    B: 'cbcmoreshells:rocket_bracket'
  }).id('createwars:cbcmoreshells/dual_he_rocket')
  event.shaped('cbcmoreshells:dual_aphe_rocket', ['RBR'], {
    R: 'cbcmoreshells:aphe_rocket',
    B: 'cbcmoreshells:rocket_bracket'
  }).id('createwars:cbcmoreshells/dual_aphe_rocket')
})
