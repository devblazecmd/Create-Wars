// Hide More Enchants' leftover test enchantments from JEI (owner 2026-11-22: "testing enchants ... cut those").
// The enchantments themselves are neutralised server-side by kubejs/data/enchantments/enchantment/test_entity_effect/*
// (apply to no item, no effects). Data-driven enchantments can't be deleted from the registry by a datapack.
const CW_TEST_ENCHANTS = ['hit_block', 'location_changed', 'post_attack_aa', 'post_attack_av', 'post_attack_va',
  'post_attack_vv', 'projectile_spawned', 'tick']

RecipeViewerEvents.removeEntries('item', event => {
  CW_TEST_ENCHANTS.forEach(n => {
    event.remove(`minecraft:enchanted_book[stored_enchantments={levels:{"enchantments:test_entity_effect/${n}":1}}]`)
  })
})
