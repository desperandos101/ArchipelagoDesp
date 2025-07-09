from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions, Toggle, Range


class Calamity(Toggle):
    """Calamity mod bosses and events are shuffled"""

    display_name = "Calamity Mod Integration"
    default = False


class Getfixedboi(Toggle):
    """Generation accomodates the secret, very difficult "getfixedboi" seed"""

    display_name = """"getfixedboi" seed"""
    default = False


class Goal(Choice):
    """
    The victory condition for your run. Stuff after the goal will not be shuffled.
    Primordial Wyrm and Boss Rush are accessible relatively early, so consider "Items" or
    "Locations" accessibility to avoid getting stuck on the goal.
    """

    display_name = "Goal"
    option_wall_of_flesh = 0
    option_mechanical_bosses = 1
    option_calamitas_clone = 2
    option_plantera = 3
    option_golem = 4
    option_empress_of_light = 5
    option_lunatic_cultist = 6
    option_astrum_deus = 7
    option_moon_lord = 8
    option_providence_the_profaned_goddess = 9
    option_devourer_of_gods = 10
    option_yharon_dragon_of_rebirth = 11
    option_zenith = 12
    option_calamity_final_bosses = 13
    option_primordial_wyrm = 14
    option_boss_rush = 15
    default = 0


class JourneyMode(Toggle):
    """
    If enabled, items the player get instantly in journey mode aren't added to the pool.
    """
    display_name = "Journey Mode"
    default = False


class ToggleEvil(Choice):
    """
    Toggle how corruption/crimson locations and items are handled.
    Corruption: Allows only corruption locations/items.
    Crimson: Allows only crimson locations/items.
    Both: Allows both corruption and crimson locations/items.

    Defaults to both.
    """
    display_name = "Toggle Evil Biome"
    option_corruption = 0
    option_crimson = 1
    option_both = 2


class BiomeLocks(Toggle):
    """
    Adds biomes to the item pool, which prevents you from acquiring certain loot until you obtain their respective
    biome. This option will automatically disable if there are not enough locations for each biome.
    """
    display_name = "Biome Locks"
    default = True


class WeatherLocks(Toggle):
    """
    Adds weather conditions "Rain" and "Wind" to the item pool.
    These weather conditions, as well as Blizzards and Sandstorms respectively, will not occur until the item is received.
    """
    display_name = "Weather Locks"
    default = True


class RandomizeNPCs(Toggle):
    """
    Adds all NPCs (barring the Guide) into the item pool. Fulfilling each NPC's housing criteria is now a location.
    For example, the player must gather 50 silver coins to activate the "Merchant" location.
    """
    display_name = "Randomize NPCs"
    default = True


class RandomizeGuide(Toggle):
    """
    Adds the Guide into the item pool.
    """
    display_name = "Randomize Guide"
    default = False


class RandomizeChestLoot(Toggle):
    """
    Primary chest items are added into the item pool and replaced with checks.
    """

    display_name = "Randomize Chest Loot"
    default = True


class ToggleChestSlotsSurface(Range):
    """
    Select how many Gold or Wooden Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 20
    range_end = 100


class ToggleChestSlotsWater(Range):
    """
    Select how many Water Chest checks to add (if chests are randomized).
    """
    display_name = "Water Chest Slots"
    default = 6
    range_end = 100


class ToggleChestSlotsSky(Range):
    """
    Select how many Floating Island Chest checks to add (if chests are randomized).
    """
    display_name = "Floating Island Chest Slots"
    default = 3
    range_end = 100


class ToggleChestSlotsMushroom(Range):
    """
    Select how many Mushroom Chest checks to add (if chests are randomized).
    """
    display_name = "Mushroom Chest Slots"
    default = 3
    range_end = 100


class ToggleChestSlotsSpider(Range):
    """
    Select how many Web Covered Chest checks to add (if chests are randomized).
    """
    display_name = "Web Covered Chest Slots"
    default = 1
    range_end = 100


class ToggleChestSlotsMarble(Range):
    """
    Select how many Marble Chest checks to add (if chests are randomized).
    """
    display_name = "Marble Chest Slots"
    default = 1
    range_end = 100


class ToggleChestSlotsGranite(Range):
    """
    Select how many Granite Chest checks to add (if chests are randomized).
    """
    display_name = "Granite Chest Slots"
    default = 1
    range_end = 100


class ToggleChestSlotsFrozen(Range):
    """
    Select how many Frozen Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 7
    range_end = 100


class ToggleChestSlotsDesert(Range):
    """
    Select how many Sandstone/Pyramid Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 9
    range_end = 100


class ToggleChestSlotsJungle(Range):
    """
    Select how many Ivy/Mahogany Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 7
    range_end = 100


class ToggleChestSlotsUnderworld(Range):
    """
    Select how many Shadow Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 5
    range_end = 100


class ToggleChestSlotsDungeon(Range):
    """
    Select how many Dungeon Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 7
    range_end = 100


class RandomizeShadowOrbLoot(Range):
    """
    If above zero, shadow orb/Crimson heart items are added into the item pool and breaking orbs grants the number of checks specified.
    Defaults to ten (five items per evil biome).
    """
    display_name = "Randomize Shadow Orb Loot"
    default = 10
    range_end = 100


class ToggleEnemyBossDrops(Range):
    """
    Specify how many items defeating a boss/invasion should reward you.
    """
    display_name = "Toggle Boss Enemy Drops"
    default = 1
    range_start = 1
    range_end = 10


class ToggleEnemyCommonDrops(Range):
    """
    Reaching a target kill count for a specific common non-invasion enemy grants a check.
    Their non-consumable drops (weapons, accessories, etc.) are added to the item pool.

    Specify how many checks to add to each common enemy variety, or set to 0 to disable common enemy randomization.
    """
    display_name = "Toggle Common Enemy Drops"
    default = 1
    range_end = 100


class ToggleEnemyCommonKillCount(Range):
    """
    Specify how many kills of a specific common enemy are required to grant a check.
    """
    display_name = "Toggle Common Enemy Kill Count Requirement"
    default = 10
    range_start = 1
    range_end = 1000


class ToggleEnemyRareDrops(Range):
    """
    Reaching a target kill count for a specific rare non-invasion enemy (Tim, Doctor Bones, etc.) grants a check.
    Their non-consumable drops are added to the item pool.

    Specify how many checks to add to each rare enemy variety, or set to 0 to disable rare enemy randomization.
    """
    display_name = "Toggle Rare Enemy Drops"
    default = 0
    range_end = 100


class ToggleEnemyRareKillCount(Range):
    """
    Specify how many kills of a specific rare enemy (including particularly rare invasion/event enemies) are required to grant a check.
    """
    display_name = "Toggle Rare Enemy Kill Count Requirement"
    default = 1
    range_start = 1
    range_end = 100


class ToggleEnemyInvasionDrops(Range):
    """
    Reaching a target kill count for an invasion/event enemy (Goblin Warrior, Blood Zombie, etc.) grants a check.
    Their non-consumable drops are added to the item pool.

    Specify how many checks to add to each invasion enemy variety, or set to 0 to disable invasion enemy randomization.
    """
    display_name = "Toggle Invasion Enemy Drops"
    default = 1
    range_end = 100


class ToggleEnemyInvasionKillCount(Range):
    """
    Specify how many kills of a specific invasion enemy are required to grant a check.
    """
    display_name = "Toggle Invasion Enemy Kill Count Requirement"
    default = 50
    range_start = 1
    range_end = 1000


class ToggleEnemyMinibossDrops(Range):
    """
    Reaching a target kill count for miniboss enemies (Wandering Eye Fish, Mimics, etc.) grants a check.
    Their non-consumable drops are added to the item pool.

    Specify how many checks to add to each boss enemy variety, or set to 0 to disable boss enemy randomization.
    """
    display_name = "Toggle Miniboss Enemy Drops"
    default = 1
    range_end = 100


class ToggleEnemyMinibossDropsAll(Toggle):
    """
    When the required amount of kills is reached for a miniboss enemy to send an item, all items are sent at once.
    """

    display_name = "Send All Boss Enemy Items At Once"
    default = True


class ToggleEnemyMinibossKillCount(Range):
    """
    Specify how many kills of a specific miniboss enemy are required to grant a check.
    """
    display_name = "Toggle Miniboss Enemy Kill Count Requirement"
    default = 1
    range_start = 1
    range_end = 10


class RandomizeShopLoot(Range):
    """
    If above zero, vendor weapons/accessories are added into the item pool, and each vendor sells the check amount specified.
    Defaults to three.
    """
    display_name = "Randomize Shop Loot"
    default = 3
    range_start = 0
    range_end = 10


class RandomizeGrapplingHookAbility(Toggle):
    """
    You are unable to use grappling hooks until you receive a hook item.
    """

    display_name = "Randomize Grappling Hook"
    default = True


class EarlyAchievements(Toggle):
    """Adds checks upon collecting early Pre-Hardmode achievements. Adds many sphere 1 checks."""

    display_name = "Early Pre-Hardmode achievements"
    default = False


class NormalAchievements(Toggle):
    """
    Adds checks upon collecting achivements not covered by the other options. Achievements for
    clearing bosses and events are excluded.
    """

    display_name = "Normal achievements"
    default = False


class GrindyAchievements(Toggle):
    """Adds checks upon collecting grindy achievements"""

    display_name = "Grindy achievements"
    default = False


class FishingAchievements(Toggle):
    """Adds checks upon collecting fishing quest achievements"""

    display_name = "Fishing quest achievements"
    default = False


class FillExtraChecksWith(Choice):
    """
    Applies if you have achievements enabled. "Useful Items" helps to make the early game less grindy.
    Items are rewarded to all players in your Terraria world.
    """

    display_name = "Fill Extra Checks With"
    option_coins = 0
    option_useful_items = 1
    default = 0


class ClassPreference(Choice):
    """
    Specializes the item pool towards the selected class.
    Disabled by default.
    """
    display_name = "Class Preference"
    option_disabled = 0
    option_melee = 1
    option_ranged = 2
    option_magic = 3
    option_summoning = 4
    default = 0


class RequireBootsJumpAndHook(Toggle):
    """
    Whether access to boots, a double jump, and a grappling hook are required logically before fighting a boss.
    Enabled by default.
    """
    display_name = "Require Boots, Double Jump, and Grappling Hook"
    default = True


class RequireWings(Toggle):
    """
    Whether access to wings are required logically before fighting any hardmode bosses.
    Enabled by default.
    """
    display_name = "Require Wings"
    default = True


class RequireOptimalGear(Toggle):
    """
    Whether access to optimal gear is required logically before fighting a boss.
    This option covers weapons, armor, and non-mobility accessories.
    Enabled by default. (DEPRECATED FOR NOW)
    """
    display_name = "Require Optimal Gear"
    default = True


class EpicNumber(Range):
    """
    A funny little thing! I wonder what it may do.
    """
    display_name = 'Epic Number'
    default = 50
    range_end = 100


@dataclass
class TerrariaOptions(PerGameCommonOptions):
    calamity: Calamity
    getfixedboi: Getfixedboi
    goal: Goal
    journey_mode: JourneyMode
    toggle_evil: ToggleEvil
    biome_locks: BiomeLocks
    weather_locks: WeatherLocks
    randomize_npcs: RandomizeNPCs
    randomize_guide: RandomizeGuide
    chest_loot: RandomizeChestLoot
    chest_surface: ToggleChestSlotsSurface
    chest_water: ToggleChestSlotsWater
    chest_sky: ToggleChestSlotsSky
    chest_mushroom: ToggleChestSlotsMushroom
    chest_web: ToggleChestSlotsSpider
    chest_marble: ToggleChestSlotsMarble
    chest_granite: ToggleChestSlotsGranite
    chest_frozen: ToggleChestSlotsFrozen
    chest_desert: ToggleChestSlotsDesert
    chest_jungle: ToggleChestSlotsJungle
    chest_underworld: ToggleChestSlotsUnderworld
    chest_dungeon: ToggleChestSlotsDungeon
    orb_loot: RandomizeShadowOrbLoot
    enemy_common_drops: ToggleEnemyCommonDrops
    enemy_common_count: ToggleEnemyCommonKillCount
    enemy_rare_drops: ToggleEnemyRareDrops
    enemy_rare_count: ToggleEnemyRareKillCount
    enemy_invasion_drops: ToggleEnemyInvasionDrops
    enemy_invasion_count: ToggleEnemyInvasionKillCount
    enemy_miniboss_drops: ToggleEnemyMinibossDrops
    enemy_miniboss_drops_all: ToggleEnemyMinibossDropsAll
    enemy_miniboss_count: ToggleEnemyMinibossKillCount
    shop_loot: RandomizeShopLoot
    grappling_hook: RandomizeGrapplingHookAbility
    early_achievements: EarlyAchievements
    normal_achievements: NormalAchievements
    grindy_achievements: GrindyAchievements
    fishing_achievements: FishingAchievements
    fill_extra_checks_with: FillExtraChecksWith
    class_preference: ClassPreference
    require_boots_jump_hook: RequireBootsJumpAndHook
    require_wings: RequireWings
    require_optimal_gear: RequireOptimalGear
    epic_number: EpicNumber
    death_link: DeathLink
