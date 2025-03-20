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


class ToggleEvil(Choice):
    """
    Toggle how corruption/crimson items are distributed in the world.
    Corruption: Allows only corruption items in the item pool, excluding crimson items.
    Crimson: Allows only crimson items in the item pool, excluding corruption items.
    Both: Allows both corruption and crimson items in the item pool.

    Defaults to both.
    """
    display_name = "Toggle Evil Biome"
    option_corruption = 0
    option_crimson = 1
    option_both = 2


class ReceiveDangerousEventsAsItems(Choice):
    """
    Toggle which events will be received as manual trigger items instead.
    All: Hardmode, All invasions, Blood Moon, Solar Eclipse.
    Hardmode Only: The only event out of the above list that will not activate when received is Hardmode.
    None: All events activate once received.
    Hardmode events will not activate until Hardmode itself is active.
    """
    display_name = "Receive Dangerous Events As Items"
    option_all = 2
    option_hardmode = 1
    option_none = 0
    default = 2


class BiomeLocks(Toggle):
    """
    Adds biomes to the item pool, which prevents you from acquiring certain loot until you obtain their respective biome.
    This option will automatically disable if there are not enough locations for each biome.
    """
    display_name = "Biome Locks"
    default = True


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
    range_end = 50


class ToggleChestSlotsWater(Range):
    """
    Select how many Water Chest checks to add (if chests are randomized).
    """
    display_name = "Water Chest Slots"
    default = 6
    range_end = 50


class ToggleChestSlotsSky(Range):
    """
    Select how many Floating Island Chest checks to add (if chests are randomized).
    """
    display_name = "Floating Island Chest Slots"
    default = 3
    range_end = 50


class ToggleChestSlotsFrozen(Range):
    """
    Select how many Frozen Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 7
    range_end = 50


class ToggleChestSlotsDesert(Range):
    """
    Select how many Sandstone/Pyramid Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 9
    range_end = 50


class ToggleChestSlotsJungle(Range):
    """
    Select how many Ivy/Mahogany Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 7
    range_end = 50


class ToggleChestSlotsUnderworld(Range):
    """
    Select how many Shadow Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 5
    range_end = 50


class ToggleChestSlotsDungeon(Range):
    """
    Select how many Dungeon Chest checks to add (if chests are randomized).
    """
    display_name = "Gold or Wooden Chest Slots"
    default = 7
    range_end = 50


class RandomizeShadowOrbLoot(Range):
    """
    If above zero, shadow orb/Crimson heart items are added into the item pool and breaking orbs grants checks.
    Defaults to ten (five items per evil biome).
    """
    display_name = "Randomize Shadow Orb Loot"
    default = 10
    range_end = 20


class RandomizeGrapplingHooks(Toggle):
    """
    The ability to use grappling hooks is added to the item pool.
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
    default = 1


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
    toggle_evil: ToggleEvil
    events_as_items: ReceiveDangerousEventsAsItems
    biome_locks: BiomeLocks
    chest_loot: RandomizeChestLoot
    chest_surface: ToggleChestSlotsSurface
    chest_water: ToggleChestSlotsWater
    chest_sky: ToggleChestSlotsSky
    chest_frozen: ToggleChestSlotsFrozen
    chest_desert: ToggleChestSlotsDesert
    chest_jungle: ToggleChestSlotsJungle
    chest_underworld: ToggleChestSlotsUnderworld
    chest_dungeon: ToggleChestSlotsDungeon
    orb_loot: RandomizeShadowOrbLoot
    grappling_hook: RandomizeGrapplingHooks
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
