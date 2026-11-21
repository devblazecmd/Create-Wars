---
tags: [bug/status/fixed, bug/severity/critical, bug/type/crash, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Shaolib|Shaolib]]", "[[../01-Mods/Synaxis|Synaxis]]", "[[../01-Mods/Create The Air War|Create The Air War]]", "[[../01-Mods/CBC Military Supplement|CBC Military Supplement]]"]
date_opened: "2026-11-21"
date_resolved: "2026-11-21"
---

# Explosions crash - Shaolib missing Synaxis

## Symptom
The server crashes ("Ticking entity") when a [[../01-Mods/Create The Air War|Create: The Air War]]
Tomahawk missile explodes:
```
java.lang.NoClassDefFoundError: com/verr1/synaxis/foundation/physics/SynaxisPhysics
  at shaolib@0.1.0/com.verr1.shaolib.compat.synaxis.SynaxisBlockBodyResolver.bodyId
  at ...ExplosionDamageCalculator.handler$...$shaolib$applyBodyExplosionResistanceModifier
  at create_the_air_wars@5.00/hi.util.ExplosionUtils.explodeProjectileImpact
```

## Reproduction
1. Without Synaxis installed, launch a Tomahawk and let it hit a block. Crashed twice in a row
   (crash-2026-11-21_02.52.10 / 02.53.03).

## Environment
- Pack version / commit: after `c6a84e1`
- Affected mod versions: Shaolib 0.1.0, Create: The Air War 5.00

## Root cause
[[../01-Mods/Shaolib|Shaolib]] 0.1.0's constructor always registers
`CompositeBlockBodyResolver.of(SableBlockBodyResolver, SynaxisBlockBodyResolver)`, with no
`ModList.isLoaded("synaxis")` check, and it doesn't declare Synaxis as a dependency. Its
`ExplosionDamageCalculator` mixin runs for every server-side explosion. For any block not on a Sable body, the Sable
resolver returns empty, falls through to the Synaxis resolver, and crashes on the missing class. The
Tomahawk is just the trigger. From the bytecode, **any** explosion on a normal block (TNT, creepers, CBC
shells) should hit the same path; only the Tomahawk was actually observed.

## Fix
Added [[../01-Mods/Synaxis|Synaxis]] `1.6.3` (same author as Shaolib) plus its requirements
[[../01-Mods/LDLib2|LDLib2]] `2.2.46.a` and [[../01-Mods/Sable Photomancy|Sable Photomancy]] `1.0.1`
(mod ID `sable_schematic_api`). Verified with `javap` that Synaxis 1.6.3 has the exact signatures Shaolib
calls (`SynaxisPhysics.bodyAt(Level, BlockPos)` and `BodyId.isGround()`). Boot + world load is clean;
**re-test the Tomahawk explosion in game to confirm.**

Worth reporting upstream to Shaolib: Synaxis should be an optional, guarded integration. Once that's
fixed, Synaxis could become optional again.

## Related
- Re-check on every Shaolib/Synaxis update: if Synaxis renames `SynaxisPhysics.bodyAt` or `BodyId`, this
  crash comes back.
