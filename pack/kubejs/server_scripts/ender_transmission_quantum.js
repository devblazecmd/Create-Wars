// Create: Ender Transmission becomes quantum tech (owner 2026-11-22: "ender trans should be a quantum thing and
// its recipes need to be adjusted to call for more quantum items to make it hard to get").
// Wireless item/fluid/rotation links across any distance or dimension, plus a chunk loader, are strong in a war
// pack, so they sit after the Entity Teleporter in the Quantum Expansion.
// Original transmitters: 5x5 mechanical crafting of obsidian, 4 ender pearls, an ender eye, 2 precision
// mechanisms and the chute/pump/shaft. Original chunk loader: 8 obsidian around a beacon.
// Each transmitter now takes: 8 Quantum Casings, 6 Quantum Pearls, 2 Advanced Components, a Quantum Mechanism.

const ENDER_TRANSMITTERS = [
  ['item_transmitter', 'create:chute'],
  ['fluid_transmitter', 'create:mechanical_pump'],
  ['energy_transmitter', 'create:shaft']
]

ServerEvents.recipes(event => {
  ENDER_TRANSMITTERS.forEach(tr => {
    event.remove({ id: 'createendertransmission:mechanical_crafting/' + tr[0] })
    event.custom({
      type: 'create:mechanical_crafting', accept_mirrored: false, category: 'misc',
      pattern: [
        'OCSCO',
        'CQAQC',
        'OQMQO',
        'CQAQC',
        'OCSCO'
      ],
      key: {
        O: { item: 'minecraft:obsidian' },
        C: { item: 'createteleporters:quantum_casing' },
        S: { item: tr[1] },
        Q: { item: 'createwars:quantum_pearl' },
        A: { item: 'createteleporters:advanced_part' },
        M: { item: 'createteleporters:quantum_mechanism' }
      },
      result: { id: 'createendertransmission:' + tr[0], count: 1 }
    }).id('createwars:ender_transmission/' + tr[0])
  })

  event.remove({ id: 'createendertransmission:crafting/chunk_loader' })
  event.shaped('createendertransmission:chunk_loader', ['CQC', 'QBQ', 'CMC'], {
    C: 'createteleporters:quantum_casing',
    Q: 'createwars:quantum_pearl',
    B: 'minecraft:beacon',
    M: 'createteleporters:quantum_mechanism'
  }).id('createwars:ender_transmission/chunk_loader')
})
