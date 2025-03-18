from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions, Toggle


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


class ReceiveDangerousEventsAsItems(Choice):
    """
    Toggle which events will be received as manual trigger items instead.
    All: Hardmode, All invasions, Blood Moon, Solar Eclipse.
    Hardmode Only: The only event out of the above list that will not activate when received is Hardmode.
    None: All events activate once received.
    Hardmode events will not activate automatically until Hardmode itself is active.
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


class RandomizeShadowOrbLoot(Toggle):
    """
    Shadow orb/Crimson heart items are added into the item pool and breaking orbs grant checks.
    """
    display_name = "Randomize Shadow Orb Loot"
    default = True


class RandomizeGrapplingHooks(Toggle):
    """
    The ability to use grappling hooks is added to the item pool.
    """

    display_name = "Randomize Grappling Hook"
    default = False


class EarlyAchievements(Toggle):
    """Adds checks upon collecting early Pre-Hardmode achievements. Adds many sphere 1 checks."""

    display_name = "Early Pre-Hardmode achievements"
    default = True


class NormalAchievements(Toggle):
    """
    Adds checks upon collecting achivements not covered by the other options. Achievements for
    clearing bosses and events are excluded.
    """

    display_name = "Normal achievements"
    default = True


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


@dataclass
class TerrariaOptions(PerGameCommonOptions):
    calamity: Calamity
    getfixedboi: Getfixedboi
    goal: Goal
    events_as_items: ReceiveDangerousEventsAsItems
    biome_locks: BiomeLocks
    chest_loot: RandomizeChestLoot
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
    death_link: DeathLink
