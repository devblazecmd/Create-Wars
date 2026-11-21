---
tags: [design]
---

# Quantum Pearl

**Item:** `createwars:quantum_pearl`, the pack's first custom item, registered by KubeJS.

| Part | File |
|---|---|
| Item registration | `pack/kubejs/startup_scripts/createwars_items.js` |
| Recipe | `pack/kubejs/server_scripts/quantum_pearl_recipe.js` |
| Texture | `pack/kubejs/assets/createwars/textures/item/quantum_pearl.png` |
| Name | `pack/kubejs/assets/createwars/lang/en_us.json` |

## Recipe
Create mixing (Basin + Mechanical Mixer, no heat): **Ender Pearl + 250 mB Telejuice → Quantum Pearl**.
Telejuice is Create: Teleporters' Quantum Fluid (`createteleporters:quantum_fluid`), made by heated
mixing of chorus fruit + water.

## Item
- Stacks to 16 (like ender pearls), uncommon rarity (aqua name).
- **Crafting ingredient only.** It is not throwable and does not teleport. Making it behave like an ender
  pearl would need custom code beyond a basic KubeJS item.
- Texture: original 16x16 pixel art drawn for the pack (purple pearl, dark rim, glowing swirl core,
  top-left highlight). Not derived from vanilla's ender pearl texture.

## Uses
All in `pack/kubejs/server_scripts/waystones_quantum.js` (see [[../01-Mods/Waystones|Waystones]]):
all 10 waystone variants (3 each), Warp Stone (7), Warp Dust, Deepslate/Dormant Shard, Warp Scroll.

## Quantum Paper
`createwars:quantum_paper`, registered in the same startup script. **Paper + 100 mB Telejuice via
Spout filling** (`createwars:filling/quantum_paper`, in `waystones_quantum.js`). Original 16x16 purple paper texture
(`kubejs/assets/createwars/textures/item/quantum_paper.png`). Replaces Paper in all 5 Waystones scroll
recipes (see [[../01-Mods/Waystones|Waystones]]).

## Notes
- `createwars` is the pack's own namespace. Future custom items/recipes should use it too.
- Startup scripts only reload on a full game restart, not `/reload`.
