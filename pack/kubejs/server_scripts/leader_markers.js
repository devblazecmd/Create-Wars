// Make Enhanced AI "leader" mobs easy to spot (owner 2026-11-22): a red glowing outline. No name tag, no boss bar
// (owner changed their mind: "no red tag and no boss bar").
// Leaders are ~2% of zombies/skeletons (entity tag enhancedai:mobs/leaders): 4x health, +10 armor, call reinforcements,
// and already wear a banner. Enhanced AI exposes insane96mcp.enhancedai.module.mobs.Leaders.isLeader(LivingEntity).
// Glow = setGlowingTag(true) (saved with the mob) + scoreboard team "cw_leaders" coloured red (outline colour comes from
// the team). No custom name, so leaders still despawn like normal mobs.
// Rhino note: no const/let inside nested blocks; keep per-entity work in top-level functions.

const LeadersClass = Java.loadClass('insane96mcp.enhancedai.module.mobs.Leaders')
const ChatFormatting = Java.loadClass('net.minecraft.ChatFormatting')
const TagKey = Java.loadClass('net.minecraft.tags.TagKey')
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
const RegistriesClass = Java.loadClass('net.minecraft.core.registries.Registries')

const LEADER_TAG = TagKey.create(RegistriesClass.ENTITY_TYPE, ResourceLocation.parse('enhancedai:mobs/leaders'))
const LEADER_TEAM = 'cw_leaders'

function cwLeaderTeam(server) {
  const sb = server.getScoreboard()
  let team = sb.getPlayerTeam(LEADER_TEAM)
  if (team == null) {
    team = sb.addPlayerTeam(LEADER_TEAM)
    team.setColor(ChatFormatting.RED)
  }
  return team
}

function cwMarkLeader(entity) {
  if (entity.isRemoved() || !entity.isAlive() || !LeadersClass.isLeader(entity)) return
  const server = entity.level().getServer()
  entity.setGlowingTag(true)
  server.getScoreboard().addPlayerToTeam(entity.getScoreboardName(), cwLeaderTeam(server))
}

function cwUnteamLeader(entity) {
  const sb = entity.level().getServer().getScoreboard()
  const team = sb.getPlayerTeam(LEADER_TEAM)
  if (team != null && sb.getPlayersTeam(entity.getScoreboardName()) == team) {
    sb.removePlayerFromTeam(entity.getScoreboardName(), team)
  }
}

EntityEvents.spawned(event => {
  const entity = event.entity
  if (!entity.getType().is(LEADER_TAG)) return
  // Enhanced AI decides leadership when the mob joins the level; check a moment later.
  event.level.getServer().scheduleInTicks(2, () => cwMarkLeader(entity))
})

// keep the scoreboard team from filling up with dead leaders
EntityEvents.death(event => {
  const entity = event.entity
  if (entity.getType().is(LEADER_TAG)) cwUnteamLeader(entity)
})
