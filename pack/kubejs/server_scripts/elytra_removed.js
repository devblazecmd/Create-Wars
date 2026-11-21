// Removes elytras from the pack. Project owner decision 2026-11-21: air travel should go through
// Create Aeronautics vehicles, not personal gliding. See vault/03-Design/Elytra Removal.md.
//
// Elytras have no recipe and no loot-table entry (vanilla or modded, checked 2026-11-21). The only
// natural source is the item frame placed with End City ships. So:
//  1. Empty any (glow) item frame holding an elytra when it joins the world (covers ships generated or
//     loaded from disk).
//  2. Backstop: stop elytra gliding outright, so elytras already in a world, from /give, or from creative
//     do nothing.
//  3. Hide from JEI.

const clearElytraFrame = event => {
  const frame = event.entity
  if (frame.item.id == 'minecraft:elytra') {
    frame.setItem(Item.of('minecraft:air'))
  }
}
EntityEvents.spawned('minecraft:item_frame', clearElytraFrame)
EntityEvents.spawned('minecraft:glow_item_frame', clearElytraFrame)

PlayerEvents.tick(event => {
  const player = event.player
  if (player.isFallFlying()) {
    player.stopFallFlying()
  }
})

ServerEvents.recipes(event => {
  event.remove({ output: 'minecraft:elytra' })
})

ServerEvents.tags('item', event => {
  event.add('c:hidden_from_recipe_viewers', 'minecraft:elytra')
})
