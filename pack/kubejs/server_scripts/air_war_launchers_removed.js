// Removes Create: The Air War's launchers and their ammo from survival.
// Project owner decision 2026-11-21. See vault/01-Mods/Create The Air War.md.
// Recipes are removed and the items hidden from JEI (via the c:hidden_from_recipe_viewers convention tag).
// Items that already exist in a world, or come from /give or creative, are not deleted.
const AIR_WAR_LAUNCHERS_AND_AMMO = [
  'create_the_air_wars:anti_aircraft_launcher', // Anti-Aircraft Launcher (no recipe upstream, creative-only)
  'create_the_air_wars:c75',                    // C-75 Rocket, its ammo (no recipe upstream)
  'create_the_air_wars:vihr',                   // Vihr Missile Launcher
  'create_the_air_wars:vihr_rocket',            // Vihr Missile, its ammo
  'create_the_air_wars:heattrap',               // Heat Trap (flare) Launcher
  'create_the_air_wars:heattrap_charge'         // Heat Charge, its ammo
]

ServerEvents.recipes(event => {
  AIR_WAR_LAUNCHERS_AND_AMMO.forEach(id => event.remove({ output: id }))
})

ServerEvents.tags('item', event => {
  event.add('c:hidden_from_recipe_viewers', AIR_WAR_LAUNCHERS_AND_AMMO)
})
