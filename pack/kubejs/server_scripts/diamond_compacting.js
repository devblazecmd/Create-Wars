// Diamond from coal via Create: superheated compacting (press + basin + blaze burner fed blaze cake).
// Why: no mod in the pack produces diamonds, only crushes diamond ore. See vault/03-Design/Diamond Recipe.md.
// KubeJS Create addon is not installed, so this uses raw Create 6 recipe JSON.
ServerEvents.recipes(event => {
  let ingredients = []
  for (let i = 0; i < 9; i++) ingredients.push({ item: 'minecraft:coal_block' })

  event.custom({
    type: 'create:compacting',
    heat_requirement: 'superheated',
    ingredients: ingredients,
    results: [{ id: 'minecraft:diamond' }]
  }).id('createwars:compacting/diamond_from_coal_blocks')
})
