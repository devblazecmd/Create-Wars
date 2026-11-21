// Pack custom items (createwars namespace).
// Quantum Pearl: Ender Pearl mixed with Telejuice (Create: Teleporters' Quantum Fluid).
// Crafting ingredient only (not throwable). Recipe: server_scripts/quantum_pearl_recipe.js.
// Texture: assets/createwars/textures/item/quantum_pearl.png (original 16x16 purple pearl).
// Startup scripts only load on game start, so a restart is needed after changes.
StartupEvents.registry('item', event => {
  event.create('createwars:quantum_pearl')
    .maxStackSize(16)
    .rarity('uncommon')

  // Quantum Paper: Paper filled with Telejuice. Used for Waystones scrolls. Recipe:
  // server_scripts/waystones_quantum.js.
  event.create('createwars:quantum_paper')
    .rarity('uncommon')
})
