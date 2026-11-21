// Quantum Pearl = Ender Pearl + 250 mB Telejuice, mixed in a Basin (no heat).
// Item registered in startup_scripts/createwars_items.js.
ServerEvents.recipes(event => {
  event.custom({
    type: 'create:mixing',
    ingredients: [
      { item: 'minecraft:ender_pearl' },
      { type: 'neoforge:single', amount: 250, fluid: 'createteleporters:quantum_fluid' }
    ],
    results: [{ id: 'createwars:quantum_pearl' }]
  }).id('createwars:mixing/quantum_pearl')
})
